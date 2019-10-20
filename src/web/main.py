import os
from flask import Flask
from flask.templating import render_template

from .drone_event_thread import DroneEventThread
from .commands import Command, CommandName

app = Flask(__name__)
drone_thread = DroneEventThread()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html.j2')


@app.route('/hello/<name>', methods=['GET'])
def hello(name):
    drone_thread.send(
        Command(CommandName.SayHello,
                {'name': name})
    )
    return name


@app.route('/flights/new', methods=['GET'])
def create_flight():
    drone_thread.send(
        Command(CommandName.StartFlight,
                {'pilot': {'name': 'Nathan'}})
    )
    return ''


@app.route('/flights/stop', methods=['GET'])
def stop_flight():
    drone_thread.send(Command(CommandName.StopFlight))
    return ''


def has_flask_auto_reload_started():
    return os.environ.get('WERKZEUG_RUN_MAIN') == 'true'


def main():
    if has_flask_auto_reload_started():
        drone_thread.start()
    app.run(host='localhost', port='8000', debug=True)
    print('Stopping app')


if __name__ == '__main__':
    main()
