from cv2 import cv2
import sys
import threading
import av
import numpy
import time
import traceback
from drone import TelloDrone
from drone_data import DroneData


class Video:
    _drone = None
    _drone_data = None
    _current_image = None
    _new_image = None
    _run_video_thread = True

    def __init__(self, drone: TelloDrone, drone_data: DroneData):
        print('VIDEO initializing')
        self._drone = drone
        self._drone_data = drone_data

    def start(self):
        threading.Thread(target=self._video_thread, daemon=True).start()

    def quit(self):
        cv2.destroyAllWindows()
        self._run_video_thread = False

    def draw(self):
        if self._new_image is not None and self._current_image is not self._new_image:
              cv2.imshow('Tello', self._new_image)
              self._current_image = self._new_image
              cv2.waitKey(1)

    def _video_thread(self):
        print('VIDEO start thread')
        container = None
        try:
            container = av.open(self._drone.get_video_stream())
            # skip first 300 frames
            frame_skip = 300
            while self._run_video_thread:
                for frame in container.decode(video=0):
                    if 0 < frame_skip:
                        frame_skip = frame_skip - 1
                        continue
                    start_time = time.time()
                    image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)

                    flight_data = self._drone_data.flight_data
                    log_data = self._drone_data.log_data

                    if flight_data:
                        self._draw_text(image, 'Flight Data: ' + str(flight_data), 0)

                    if log_data:
                        self._draw_text(image, 'MVO: ' + str(log_data.mvo), -3)
                        self._draw_text(image, ('IMU: ' + str(log_data.imu))[0:52], -2)
                        self._draw_text(image, '     ' + ('IMU: ' + str(log_data.imu))[52:], -1)

                    self._new_image = image

                    if frame.time_base < 1.0/60:
                        time_base = 1.0/60
                    else:
                        time_base = frame.time_base
                    frame_skip = int((time.time() - start_time)/time_base)
        except Exception as ex:
            print('VIDEO exception:')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            print(ex)

        print('VIDEO stop thread')

    def _draw_text(image, text, row):
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        font_size = 24
        font_color = (255,255,255)
        bg_color = (0,0,0)
        d = 2
        height, width = image.shape[:2]
        left_mergin = 10
        if row < 0:
            pos =  (left_mergin, height + font_size * row + 1)
        else:
            pos =  (left_mergin, font_size * (row + 1))
        cv2.putText(image, text, pos, font, font_scale, bg_color, 6)
        cv2.putText(image, text, pos, font, font_scale, font_color, 1)
