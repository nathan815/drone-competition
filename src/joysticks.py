import pygame
from drone import TelloDrone


class Controller:
    pass


class FightPad(Controller):
    # d-pad
    UP = -1  # UP
    DOWN = -1  # DOWN
    ROTATE_LEFT = -1  # LEFT
    ROTATE_RIGHT = -1  # RIGHT

    # bumper triggers
    TAKEOFF = 5  # R1
    LAND = 4  # L1
    # UNUSED = 7 #R2
    # UNUSED = 6 #L2

    # buttons
    FORWARD = 3  # TRIANGLE
    BACKWARD = 1  # CROSS
    LEFT = 0  # SQUARE
    RIGHT = 2  # CIRCLE

    # axis
    LEFT_X = 0
    LEFT_Y = 1
    RIGHT_X = 2
    RIGHT_Y = 3
    LEFT_X_REVERSE = -1.0
    LEFT_Y_REVERSE = -1.0
    RIGHT_X_REVERSE = 1.0
    RIGHT_Y_REVERSE = -1.0
    DEADZONE = 0.05


class JoystickPS3(Controller):
    # d-pad
    UP = 4  # UP
    DOWN = 6  # DOWN
    ROTATE_LEFT = 7  # LEFT
    ROTATE_RIGHT = 5  # RIGHT

    # bumper triggers
    TAKEOFF = 11  # R1
    LAND = 10  # L1
    # UNUSED = 9 #R2
    # UNUSED = 8 #L2

    # buttons
    FORWARD = 12  # TRIANGLE
    BACKWARD = 14  # CROSS
    LEFT = 15  # SQUARE
    RIGHT = 13  # CIRCLE

    # axis
    LEFT_X = 0
    LEFT_Y = 1
    RIGHT_X = 2
    RIGHT_Y = 3
    LEFT_X_REVERSE = 1.0
    LEFT_Y_REVERSE = -1.0
    RIGHT_X_REVERSE = 1.0
    RIGHT_Y_REVERSE = -1.0
    DEADZONE = 0.1


class JoystickPS4(Controller):
    # d-pad
    UP = -1  # UP
    DOWN = -1  # DOWN
    ROTATE_LEFT = -1  # LEFT
    ROTATE_RIGHT = -1  # RIGHT

    # bumper triggers
    TAKEOFF = 5  # R1
    LAND = 4  # L1
    # UNUSED = 7 #R2
    # UNUSED = 6 #L2

    # buttons
    FORWARD = 3  # TRIANGLE
    BACKWARD = 1  # CROSS
    LEFT = 0  # SQUARE
    RIGHT = 2  # CIRCLE

    # axis
    LEFT_X = 0
    LEFT_Y = 1
    RIGHT_X = 2
    RIGHT_Y = 3
    LEFT_X_REVERSE = 1.0
    LEFT_Y_REVERSE = -1.0
    RIGHT_X_REVERSE = 1.0
    RIGHT_Y_REVERSE = -1.0
    DEADZONE = 0.08


class JoystickPS4Alt(Controller):
    # d-pad
    UP = -1  # UP
    DOWN = -1  # DOWN
    ROTATE_LEFT = -1  # LEFT
    ROTATE_RIGHT = -1  # RIGHT

    # bumper triggers
    TAKEOFF = 5  # R1
    LAND = 4  # L1
    # UNUSED = 7 #R2
    # UNUSED = 6 #L2

    # buttons
    FORWARD = 3  # TRIANGLE
    BACKWARD = 1  # CROSS
    LEFT = 0  # SQUARE
    RIGHT = 2  # CIRCLE

    # axis
    LEFT_X = 0
    LEFT_Y = 1
    RIGHT_X = 3
    RIGHT_Y = 4
    LEFT_X_REVERSE = 1.0
    LEFT_Y_REVERSE = -1.0
    RIGHT_X_REVERSE = 1.0
    RIGHT_Y_REVERSE = -1.0
    DEADZONE = 0.08


class JoystickF310(Controller):
    # d-pad
    UP = -1  # UP
    DOWN = -1  # DOWN
    ROTATE_LEFT = -1  # LEFT
    ROTATE_RIGHT = -1  # RIGHT

    # bumper triggers
    TAKEOFF = 5  # R1
    LAND = 4  # L1
    # UNUSED = 7 #R2
    # UNUSED = 6 #L2

    # buttons
    FORWARD = 3  # Y
    BACKWARD = 0  # B
    LEFT = 2  # X
    RIGHT = 1  # A

    # axis
    LEFT_X = 0
    LEFT_Y = 1
    RIGHT_X = 3
    RIGHT_Y = 4
    LEFT_X_REVERSE = 1.0
    LEFT_Y_REVERSE = -1.0
    RIGHT_X_REVERSE = 1.0
    RIGHT_Y_REVERSE = -1.0
    DEADZONE = 0.08

class JoystickXboxOne(Controller):
    # d-pad
    UP = 0  # UP
    DOWN = 1  # DOWN
    ROTATE_LEFT = 2  # LEFT
    ROTATE_RIGHT = 3  # RIGHT

    # bumper triggers
    TAKEOFF = 9  # RB
    LAND = 8  # LB
    # UNUSED = 7 #RT
    # UNUSED = 6 #LT

    # buttons
    FORWARD = 14  # Y
    BACKWARD = 11  # A
    LEFT = 13  # X
    RIGHT = 12  # B

    # axis
    LEFT_X = 0
    LEFT_Y = 1
    RIGHT_X = 2
    RIGHT_Y = 3
    LEFT_X_REVERSE = 1.0
    LEFT_Y_REVERSE = -1.0
    RIGHT_X_REVERSE = 1.0
    RIGHT_Y_REVERSE = -1.0
    DEADZONE = 0.09


class JoystickTaranis(Controller):
    # d-pad
    UP = -1  # UP
    DOWN = -1  # DOWN
    ROTATE_LEFT = -1  # LEFT
    ROTATE_RIGHT = -1  # RIGHT

    # bumper triggers
    TAKEOFF = 12  # left switch
    LAND = 12  # left switch
    # UNUSED = 7 #RT
    # UNUSED = 6 #LT

    # buttons
    FORWARD = -1
    BACKWARD = -1
    LEFT = -1
    RIGHT = -1

    # axis
    LEFT_X = 3
    LEFT_Y = 0
    RIGHT_X = 1
    RIGHT_Y = 2
    LEFT_X_REVERSE = 1.0
    LEFT_Y_REVERSE = 1.0
    RIGHT_X_REVERSE = 1.0
    RIGHT_Y_REVERSE = 1.0
    DEADZONE = 0.01

class JoystickButtonHandler:
    _controller: Controller = None

    """
    Create new JoystickButtonHandler
    
    controller - one of the Controller classes above
    """
    def __init__(self, controller: Controller):
        self._controller = controller

    def handle_event(self, drone: TelloDrone, e):
        #print("Input Event:", e)
        speed = 100

        if e.type == pygame.JOYAXISMOTION:
            # ignore small input values (Deadzone)
            if -self._controller.DEADZONE <= e.value <= self._controller.DEADZONE:
                e.value = 0.0
            if e.axis == self._controller.LEFT_Y:
                drone.set_pitch(e.value * self._controller.LEFT_Y_REVERSE)
            elif e.axis == self._controller.LEFT_X:
                drone.set_roll(e.value * self._controller.LEFT_X_REVERSE)
            elif e.axis == self._controller.RIGHT_Y:
                drone.set_throttle(e.value * self._controller.RIGHT_Y_REVERSE)
            elif e.axis == self._controller.RIGHT_X:
                drone.set_yaw(e.value * self._controller.RIGHT_X_REVERSE)

        elif e.type == pygame.JOYHATMOTION:
            if e.value[0] < 0:
                drone.counter_clockwise(speed)
            if e.value[0] == 0:
                drone.clockwise(0)
            if e.value[0] > 0:
                drone.clockwise(speed)

            if e.value[1] < 0:
                drone.down(speed)
            if e.value[1] == 0:
                drone.up(0)
            if e.value[1] > 0:
                drone.up(speed)

        elif e.type == pygame.JOYBUTTONDOWN:
            if e.button == self._controller.LAND:
                drone.land()
            elif e.button == self._controller.UP:
                drone.up(speed)
            elif e.button == self._controller.DOWN:
                drone.down(speed)
            elif e.button == self._controller.ROTATE_RIGHT:
                drone.clockwise(speed)
            elif e.button == self._controller.ROTATE_LEFT:
                drone.counter_clockwise(speed)
            elif e.button == self._controller.FORWARD:
                drone.forward(speed)
            elif e.button == self._controller.BACKWARD:
                drone.backward(speed)
            elif e.button == self._controller.RIGHT:
                drone.right(speed)
            elif e.button == self._controller.LEFT:
                drone.left(speed)

        elif e.type == pygame.JOYBUTTONUP:
            if e.button == self._controller.TAKEOFF:
                if drone.throttle != 0.0:
                    print('###')
                    print('### throttle != 0.0 (This may hinder the drone from taking off)')
                    print('###')
                drone.takeoff()
            elif e.button == self._controller.UP:
                drone.up(0)
            elif e.button == self._controller.DOWN:
                drone.down(0)
            elif e.button == self._controller.ROTATE_RIGHT:
                drone.clockwise(0)
            elif e.button == self._controller.ROTATE_LEFT:
                drone.counter_clockwise(0)
            elif e.button == self._controller.FORWARD:
                drone.forward(0)
            elif e.button == self._controller.BACKWARD:
                drone.backward(0)
            elif e.button == self._controller.RIGHT:
                drone.right(0)
            elif e.button == self._controller.LEFT:
                drone.left(0)


def joystick_controller_from_name(name: str):
    controllers = {
        "PS4": JoystickPS4,
        "Wireless Controller": JoystickPS4,
        "Sony Computer Entertainment Wireless Controller": JoystickPS4,

        "PS4Alt": JoystickPS4Alt,
        "Sony Interactive Entertainment Wireless Controller": JoystickPS4Alt,

        "PS3": JoystickPS3,
        "PLAYSTATION(R)3 Controller": JoystickPS3,
        "Sony PLAYSTATION(R)3 Controller": JoystickPS3,

        "F310": JoystickF310,
        "Logitech Gamepad F310": JoystickF310,

        "XboxOne": JoystickXboxOne,
        "Xbox One Wired Controller": JoystickXboxOne,

        "Taranis": JoystickTaranis,
        "FrSky Taranis Joystick": JoystickTaranis,

        "FightPad": FightPad,
        "Wired Fight Pad Pro for Nintendo Switch": FightPad
    }
    return controllers[name] if name in controllers else None
