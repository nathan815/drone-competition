import traceback
from os import environ

from ..core.flight_control import FlightControl, FlightConfig
from ..core.joysticks import JoystickButtonHandler, joystick_controller_from_name

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame


def run(config: FlightConfig, pilot=None):
    print('Welcome to Drone Control!')

    if pilot:
        print('\n---\nPilot Info\n' + str(pilot) + '\n---\n')

    pygame.init()
    pygame.joystick.init()

    num_joysticks = pygame.joystick.get_count()

    if num_joysticks > 0:
        print('Available Joysticks:')
    else:
        print('Error: No joysticks detected')
        return

    joystick_id = 0
    joysticks = []
    for i in range(0, num_joysticks):
        js = pygame.joystick.Joystick(i)
        joysticks.append(js)
        print(i, '-', js.get_name())

    if num_joysticks > 1:
        joystick_id = int(input('Select joystick (0-' + str(num_joysticks - 1) + '): '))

    joystick = joysticks[joystick_id]
    joystick.init()
    joystick_name = joystick.get_name()
    print('Selected Joystick: ', joystick_id, '-', joystick_name, '\n')

    joystick_controller_mapping = joystick_controller_from_name(joystick_name)
    while joystick_controller_mapping is None:
        print('Controller type not recognized.')
        manual_name = input('Select controller (PS3, PS3Alt, PS4, F310, XboxOne, Taranis, FightPad): ')
        joystick_controller_mapping = joystick_controller_from_name(manual_name)

    joystick_handler = JoystickButtonHandler(joystick_controller_mapping)
    flight_control = FlightControl(config, joystick_handler, pilot)
    flight_control.run()

    print('PROGRAM END')


def start(config: FlightConfig, pilot=None):
    try:
        run(config, pilot)
    except Exception as ex:
        print('Caught Exception:', ex)
        traceback.print_exc()


if __name__ == '__main__':
    start()
