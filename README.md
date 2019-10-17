# COSC 480 Drone Project

[![Build Status](https://travis-ci.com/nathan815/cosc480-drone.svg?token=Qny2uL81Nn96aTdZPDAH&branch=master)](https://travis-ci.com/nathan815/cosc480-drone)


    git clone https://github.com/nathan815/cosc480-drone
    cd cosc480-drone

## Installation

First, ensure [pipenv](https://pipenv-fork.readthedocs.io/en/latest/), pkg-config, ffmpeg, and mplayer are installed.

On Mac you can use Homebrew:

    brew cask install xquartz
    brew install pipenv pkg-config ffmpeg mplayer

Windows uses Chocolatey (choco) but it will be a little different than this.

Install the python dependencies using pipenv:

    pipenv install

Finally, run the program using `fly.py` entrypoint script (or `test_flight.py`) in the virtual environment:

    pipenv run python src/fly.py

Alternatively, you can start a pipenv shell:

    pipenv shell
    
And then any ocmmands will be ran in the python3 virtual environment, i.e.
    
    python src/fly.py
