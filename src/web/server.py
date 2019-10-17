from flask import Flask, escape, request
from flask.templating import render_template

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html.j2')


@app.route('/flights/new', methods=['POST'])
def create_flight():
    return 'hi'


def main():

    app.run(host='localhost', port='8000', debug=True)


if __name__ == '__main__':
    main()
