import sys
from main_program import start_drone_control
from pilot import Pilot


def fly(args):
    if len(args) == 0:
        print("usage: fly.py \"Name here\" \"Department\" \"Major\"")
        return

    name = args[0]
    department = args[1] if len(args) > 1 else ''
    major = args[2] if len(args) > 2 else ''
    pilot = Pilot(name, department, major)
    start_drone_control(pilot)


if __name__ == '__main__':
    del sys.argv[0]  # get rid of first argument, which is the script file name
    fly(sys.argv)
