import random
import sys
import threading
import time
import traceback

import av
import numpy
import cv2

from .drone import TelloDrone
from .drone import DroneEventHandler

VIDEO_FPS = 30
VIDEO_SLEEP = VIDEO_FPS / 1000


class VideoException(Exception):
    pass


class Video:

    def __init__(self, drone: TelloDrone, drone_events: DroneEventHandler):
        self._drone = drone
        self._drone_events = drone_events
        self._current_image = None
        self._video_thread = None
        self._video_thread_running = False
        self._av_container = None

    def start(self):
        if self._av_container:
            raise VideoException('Video already started')
        self._av_container = av.open(self._drone.get_video_stream())

    def start_window_video_thread(self):
        self._video_thread = threading.Thread(target=self._video_window_thread, daemon=True).start()
        self._video_thread_running = True

    def stop(self):
        cv2.destroyAllWindows()
        self._video_thread_running = False
        self._av_container = None

    def get_frame_test(self) -> bytes:
        container = av.open('/Users/nathan/Movies/Countdown.mp4')
        for frame in container.decode(video=0):
            image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)
            ret, jpeg = cv2.imencode('.jpg', image)
            yield jpeg.tobytes()
            time.sleep(VIDEO_SLEEP)

    def generate_frame_jpeg(self) -> bytes:
        for frame in self.generate_frame():
            ret, jpeg = cv2.imencode('.jpg', frame)
            yield jpeg.tobytes()

    def generate_frame(self) -> bytes:
        if not self._av_container:
            raise VideoException('Video not started')
        frame_skip = 300
        for frame in self._av_container.decode(video=0):
            if frame_skip > 0:
                frame_skip -= 1
                continue
            start_time = time.time()
            image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)

            # flight_data = self._drone_data.flight_data
            # log_data = self._drone_data.log_data
            #
            # if flight_data:
            #     self._draw_text(image, 'Flight Data: ' + str(flight_data), 0)
            #
            # if log_data:
            #     self._draw_text(image, 'MVO: ' + str(log_data.mvo), -3)
            #     self._draw_text(image, ('IMU: ' + str(log_data.imu))[0:52], -2)
            #     self._draw_text(image, '     ' + ('IMU: ' + str(log_data.imu))[52:], -1)

            if frame.time_base < 1.0 / 60:
                time_base = 1.0 / 60
            else:
                time_base = frame.time_base
            frame_skip = int((time.time() - start_time) / time_base)

            yield image
            time.sleep(VIDEO_SLEEP)

    def _video_window_thread(self):
        print('VIDEO: start window thread')
        try:
            self.start()
            while self._video_thread_running:
                image = self.generate_frame()
                if image is not self._current_image:
                    self._current_image = image
                    cv2.imshow('Drone Camera Feed', image)
                    cv2.waitKey(0)
        except Exception as ex:
            print('VIDEO exception:')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            print(ex)
        finally:
            print('VIDEO: stop window thread')
            cv2.destroyAllWindows()

    def _draw_text(self, image, text, row):
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        font_size = 24
        font_color = (255, 255, 255)
        bg_color = (0, 0, 0)
        height, width = image.shape[:2]
        left_mergin = 10
        if row < 0:
            pos = (left_mergin, height + font_size * row + 1)
        else:
            pos = (left_mergin, font_size * (row + 1))
        cv2.putText(image, text, pos, font, font_scale, bg_color, 6)
        cv2.putText(image, text, pos, font, font_scale, font_color, 1)
