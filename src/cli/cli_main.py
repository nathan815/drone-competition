import traceback
import pygame

from ..core.flight_control import FlightControl, FlightConfig
from ..core.joysticks import JoystickButtonHandler, joystick_controller_from_name
from ..core.logging_setup import *

logging.getLogger('dse').setLevel('FATAL')


def run(config: FlightConfig, pilot=None):

    flight_control = None
    try:
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
    except Exception as ex:
        print('EXCEPTION (MAIN THREAD):', ex.__class__, ex)
        print('\n -- Stack Trace -- \n')
        traceback.print_exc()
        print('\n')
    except KeyboardInterrupt:
        pass
    finally:
        if flight_control:
            flight_control.stop()

        print('MAIN THREAD EXITED')