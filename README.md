# COSC 480 Drone Project

[![Build Status](https://travis-ci.com/nathan815/cosc480-drone.svg?token=Qny2uL81Nn96aTdZPDAH&branch=master)](https://travis-ci.com/nathan815/cosc480-drone)


    git clone https://github.com/nathan815/cosc480-drone
    cd cosc480-drone

## Installation

First, ensure [pipenv](https://pipenv-fork.readthedocs.io/en/latest/), pkg-config, ffmpeg, and mplayer are installed.

On Mac you can use Homebrew:

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

will automatically run on python 3.7 with all needed dependencies, provided you followed the steps above.
