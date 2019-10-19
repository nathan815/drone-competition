import os
from flask import Flask
from flask.templating import render_template

from .drone_thread import DroneThread
from .commands import SayHello

app = Flask(__name__)
drone_thread = DroneThread()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html.j2')


@app.route('/hello/<name>', methods=['GET'])
def hello(name):
    drone_thread.send_command(SayHello({'name': name}))
    return name


@app.route('/flights/new', methods=['POST'])
def create_flight():
    return 'hi'


def has_flask_auto_reload_started():
    return os.environ.get('WERKZEUG_RUN_MAIN') == 'true'


def main():
    if has_flask_auto_reload_started():
        drone_thread.start()
    app.run(host='localhost', port='8000', debug=True)
    print('Stopping app')


if __name__ == '__main__':
    main()
