import sys
from .drone_control import start
from ..core.flight import Pilot


def fly(args):
    if len(args) == 0:
        print("usage: fly.py \"Name here\" \"Major\" \"College\" \"Group\"")
        return

    name = args[0]
    major = args[1] if len(args) > 1 else ''
    college = args[2] if len(args) > 2 else ''
    group = args[3] if len(args) > 3 else ''
    pilot = Pilot(name, major, Pilot.GroupType(group).name, college)
    start(pilot)


if __name__ == '__main__':
    del sys.argv[0]  # get rid of first argument, which is the script file name
    fly(sys.argv)
