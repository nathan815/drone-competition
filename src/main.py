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
from drone_data import DroneData

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

  joysticks = []
  for i in range(0, num_joysticks):
    js = pygame.joystick.Joystick(i)
    joysticks.append(js)
    print(i, ' - ', js.get_name())

  if num_joysticks > 1:
    joystick_id = int(input("select joystick (0-" + str(num_joysticks-1) + "): "))

  joystick = joysticks[joystick_id]
  joystick.init()
  joystick_name = joystick.get_name()
  print("Joystick Name: ", joystick_name)

  joystick_mapping = joystick_mapping_from_name(joystick_name)
  while joystick_mapping == None: 
    print("Joystick not recognized. Manually select a mapping name.")
    manual_name = input("Enter mapping (PS3, PS3Alt, PS4, F310, XboxOne, Taranis, FightPad): ")
    joystick_mapping = joystick_mapping_from_name(manual_name)

  joystick_handler = JoystickButtonHandler(joystick_mapping)

  drone = TelloDrone()

  drone_data = DroneData()
  drone.subscribe(drone.EVENT_FLIGHT_DATA, drone_data.handler)
  drone.subscribe(drone.EVENT_LOG_DATA, drone_data.handler)

  video = Video(drone, drone_data)

  print("Connecting to drone...")
  drone.connect()
  drone.wait_for_connection(60.0)
  print("Connected!")

  video.start()

  try:
    while True:

      sleep(0.01)
      for e in pygame.event.get():
        joystick_handler.handle_event(drone, e)

      video.draw()

  except KeyboardInterrupt as ex:
    print("Exiting...")
  finally:
    video.quit()
    drone.land()
    drone.quit()
    exit(0)

if __name__ == '__main__':
  try:
    main()
  except Exception as ex:
    print("Exception: ", ex)
    traceback.print_exc()
