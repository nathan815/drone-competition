from enum import Enum


class CommandName(Enum):
    SayHello = 0,
    StartFlight = 1,
    StopFlight = 2


class Command:
    def __init__(self, name: CommandName, data: dict = {}):
        self.name = name
        self.data = data
