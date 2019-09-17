# COSC 480 Drone Project

    git clone https://github.com/nathan815/COSC480-Drone
    cd COSC480-Drone

## Running/Developing with Docker

Build the docker container:
    ./build

Or
    docker build -t cosc480-drone .

Run docker container:
    ./run

Or
    docker run -it --rm --network host -v "$PWD":/app cosc480-drone

And if you need, you can run an interactive bash shell in the container:
    docker run -it --rm --network host -v "$PWD":/app --entrypoint bash cosc480-drone

## Manual Method

First, ensure pkg-config, ffmpeg, and mplayer are installed.

On Mac:
    brew install pkg-config
    brew install ffmpeg
    brew install mplayer

Use Chocolate (choco) on Windows

Install python dependencies:
    pip install -r requirements.txt

Run:
    python src/drone.py
