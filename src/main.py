from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import tellopy
import pygame
import traceback
from time import sleep
from cv2 import cv2

from drone import TelloDrone
from joysticks import JoystickButtonHandler, joystick_mapping_from_name
from video import Video

def handler(event, sender, data, **args):
  drone = sender
  if event is drone.EVENT_FLIGHT_DATA:
    print("Drone Data: ", data)

def main():
  print("Welcome to Drone Control!")
  pygame.init()
  pygame.joystick.init()

  num_joysticks = pygame.joystick.get_count()

  if(num_joysticks > 0):
    print("# of joysticks detected = ", num_joysticks)
  else:
    print("Error: No joysticks detected")
    return

  joystick_id = 0
  if num_joysticks > 1:
    joystick_id = int(input("select joystick (0-" + str(num_joysticks-1) + "): "))

  joystick = pygame.joystick.Joystick(joystick_id)
  joystick.init()
  joystick_name = joystick.get_name()
  print("Joystick Name: ", joystick_name)

  joystick_mapping = joystick_mapping_from_name(joystick_name)
  while joystick_mapping == None: 
    print("Joystick not recognized. Manually select a mapping name.")
    manual_name = input("Enter mapping (PS3, PS3Alt, PS4, F310, XboxOne, or Taranis): ")
    joystick_mapping = joystick_mapping_from_name(manual_name)

  joystick_handler = JoystickButtonHandler(joystick_mapping)

  drone = TelloDrone()
  drone.subscribe(drone.EVENT_FLIGHT_DATA, handler)

  video = Video(drone)

  video.main_thread_update()

  print("Connecting to drone...")
  drone.connect()
  drone.wait_for_connection(60.0)
  print("Connected!")

  try:
    while True:

      sleep(0.01)
      for e in pygame.event.get():
        joystick_handler.handle_event(drone, e)

      video.main_thread_update()

  except KeyboardInterrupt as ex:
    print("Exiting...")
    exit(1)
  finally:
    video.quit()
    drone.land()
    drone.quit()
    drone.quit()

if __name__ == '__main__':
  try:
    main()
  except Exception as ex:
    print("Exception: ", ex)
    traceback.print_exc()