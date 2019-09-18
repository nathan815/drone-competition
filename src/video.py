from cv2 import cv2
import threading
import av
import numpy
import time
import traceback

class Video:
    _drone = None
    _current_image = None
    _new_image = None

    _run_recv_thread = True
    _flight_data = None
    _log_data = None

    def __init__(self, drone):
        print('VIDEO initialize')
        self._drone = drone
        img = cv2.imread('/Users/nathan/Dev/cosc480/drone/src/drone.png', cv2.IMREAD_UNCHANGED)
        cv2.imshow('Tello', img)
        cv2.waitKey(0)

    def main_thread_update(self):
        if self._new_image != None and self._current_image is not self._new_image:
              cv2.imshow('Tello', self._new_image)
              self._current_image = self._new_image
              cv2.waitKey(1)

    def start_video_thread(self):
        threading.Thread(target=self.recv_thread).start()

    def quit(self):
        cv2.destroyAllWindows()
        self._run_recv_thread = False

    def recv_thread(self):
        print('VIDEO start thread')
        container = None
        try:
            container = av.open(self._drone.get_video_stream())
            # skip first 300 frames
            frame_skip = 300
            while self._run_recv_thread:
                for frame in container.decode(video=0):
                    if 0 < frame_skip:
                        frame_skip = frame_skip - 1
                        continue
                    start_time = time.time()
                    image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)

                    if self._flight_data:
                        self.draw_text(image, 'TelloPy: joystick_and_video ' + str(flight_data), 0)
                    if self._log_data:
                        self.draw_text(image, 'MVO: ' + str(log_data.mvo), -3)
                        self.draw_text(image, ('IMU: ' + str(log_data.imu))[0:52], -2)
                        self.draw_text(image, '     ' + ('IMU: ' + str(log_data.imu))[52:], -1)
                    new_image = image
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

    def draw_text(image, text, row):
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
