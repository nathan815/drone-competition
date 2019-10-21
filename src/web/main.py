import os
import threading

from flask import Flask, Response
from flask.templating import render_template
from flask_socketio import SocketIO

from .commands import Command, CommandName
from .drone_event_thread import DroneEventThread
from ..core.video import Video

app = Flask(__name__)
socketio = SocketIO(app)
drone_thread = DroneEventThread()


@app.route('/')
def index():
    return render_template('index.html.j2')


@socketio.on('flight.start')
def start_flight(data):
    pilot = data.get('pilot')
    drone_thread.send(
        Command(CommandName.StartFlight,
                {'pilot': pilot})
    )


@socketio.on('flight.stop')
def stop_flight():
    drone_thread.send(Command(CommandName.StopFlight))


@socketio.on('hello')
def hello(name):
    drone_thread.send(
        Command(CommandName.SayHello,
                {'name': name})
    )
    return name


@app.route('/video_feed')
def video_feed():
    return Response(video_feed_frame_generator(drone_thread.get_video()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def video_feed_frame_generator(video: Video):
    frame_num = 0
    for frame in video.get_frame_test():
        print('frame', frame_num, 'thread', threading.get_ident())
        frame_num += 1
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def main():
    has_flask_auto_reload_started = os.environ.get('WERKZEUG_RUN_MAIN') == 'true'
    # this conditional prevents starting drone thread twice
    if has_flask_auto_reload_started:
        drone_thread.start()
    # app.run(host='localhost', port='8000', debug=True)
    socketio.run(app, port=8000, debug=True)
    print('Stopping app')


if __name__ == '__main__':
    main()
