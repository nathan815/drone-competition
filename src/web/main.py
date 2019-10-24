import os
import threading

from flask import Flask, Response
from flask.templating import render_template
from flask_socketio import SocketIO

from .commands import Command, CommandName
from .event_thread import DroneEventThread
from ..core.logging_setup import *
from ..core.pilot import Pilot
from ..core.video import Video, VideoException

logger = logging.getLogger(__name__)

logging.getLogger('werkzeug').setLevel(logging.WARNING)
logging.getLogger('engineio').setLevel(logging.WARNING)
logging.getLogger('socketio').setLevel(logging.WARNING)

app = Flask(__name__)
socketio = SocketIO(app)
drone_thread = DroneEventThread()


@app.route('/')
def index():
    return render_template('index.html.j2')


@socketio.on('flight.start')
def start_flight(data):
    pilot_info = data.get('pilot')
    pilot = Pilot(pilot_info.get('name'),
                  pilot_info.get('department'),
                  pilot_info.get('major'),
                  pilot_info.get('school'))
    drone_thread.send(
        Command(CommandName.StartFlight,
                {'pilot': pilot})
    )


@socketio.on('flight.stop')
def stop_flight():
    drone_thread.send(Command(CommandName.StopFlight))


@app.route('/video_feed')
def video_feed():

    def video_feed_frame_generator(video: Video):
        try:
            logger.info('Start streaming video feed on thread ' + str(threading.get_ident()))
            frame_num = 1
            for frame in video.generate_frame_jpeg():
                frame_num += 1
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            logger.info(f'End of video feed ({frame_num} frames) on thread ' + str(threading.get_ident()))
        except Exception as ex:
            logger.error('Video stream generator exception: ' + ex.__class__.__name__ + ' - ' + str(ex))

    return Response(video_feed_frame_generator(drone_thread.get_video()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def main():
    has_flask_auto_reload_started = os.environ.get('WERKZEUG_RUN_MAIN') == 'true'
    # this conditional prevents starting drone thread twice at first run
    if has_flask_auto_reload_started:
        drone_thread.start()
    socketio.run(app, port=8000, debug=True)
    print('Server stopped')


if __name__ == '__main__':
    main()
