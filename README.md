# Drone Racing Competition Application

[![Build Status](https://travis-ci.com/nathan815/cosc480-drone.svg?token=Qny2uL81Nn96aTdZPDAH&branch=master)](https://travis-ci.com/nathan815/cosc480-drone)

Authors: Nathan Johnson, Ben Potter

This application uses tellopy to control a drone. It includes a web app to allow the competition volunteer to enter pilot details, start/stop flights, mark flights as valid/invalid, view the live video feed, etc. All flight data is stored in Cassandra in real time. A separate [leaderboard application](https://github.com/nathan815/drone-leaderboard) reads from Cassandra and displays the top pilots and other competition stats. 

This is a semester-long project for COSC 480 Cloud Computing.

## Technical Info
* Our Cassandra cluster consists of 3 nodes running on AWS EC2 instances.
* The volunteer/flight control web app is built with Flask, flask-socketio, and React.
* [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/) is used to manage our python depenencies.

## Installation

    git clone https://github.com/nathan815/cosc480-drone
    cd cosc480-drone

First, install [pipenv](https://pipenv-fork.readthedocs.io/en/latest/), pkg-config, ffmpeg, and mplayer.

If you're on macOS, you can use Homebrew:

    brew cask install xquartz
    brew install pipenv pkg-config ffmpeg mplayer

On Windows, there is the Chocolatey (choco) package manager which is similar to Homebrew but it will be a little different.

Install the python dependencies using pipenv:

    pipenv install

Finally, run the program using `fly` or `test_flight` entrypoint shell scripts:

    ./fly "Pilot Name" "Department" "Major"
    ./test_flight

## Pipenv stuff 
You can start a pipenv shell:

    pipenv shell
    
And then any commands will be ran in the context of the python3 virtual environment. 

For example, if you're in the pipenv shell, then
    
    python -m src.cli.test_flight

will automatically run in the python 3.7 virtual env with all needed dependencies.
