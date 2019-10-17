# COSC 480 Drone Project

[![Build Status](https://travis-ci.com/nathan815/cosc480-drone.svg?token=Qny2uL81Nn96aTdZPDAH&branch=master)](https://travis-ci.com/nathan815/cosc480-drone)


    git clone https://github.com/nathan815/cosc480-drone
    cd cosc480-drone

## Installation

First, ensure python, pkg-config, ffmpeg, and mplayer are installed.

On Mac you can use Homebrew:

    brew cask install xquartz
    brew install pkg-config ffmpeg mplayer

(Use Chocolatey (choco) on Windows)

[Install pipenv](https://pipenv-fork.readthedocs.io/en/latest/).

Install the python dependencies using pipenv:

    pipenv install

Run the `fly.py` entrypoint script (or `test_flight.py`) in the virtual environment:

    pipenv run python src/fly.py

Alternatively, you can start a pipenv shell:

    pipenv shell
    
And then any ocmmands will be ran in the python3 virtual environment, i.e.
    
    python src/fly.py
