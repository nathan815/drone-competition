FROM python:3

RUN apt-get update && apt-get install -y \
  python-dev \
  pkg-config \
  libavformat-dev libavcodec-dev libavdevice-dev \
  libavutil-dev libswscale-dev libswresample-dev libavfilter-dev \
  ffmpeg \
  mplayer \
  && apt-get clean && apt-get autoclean

RUN python -m pip install --upgrade setuptools pip wheel

WORKDIR /app
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "src/main.py" ]
