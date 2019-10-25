from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID


@dataclass
class Pilot:

    class GroupType(Enum):
        Student = 'student'
        Staff = 'staff'
        Professor = 'professor'

    name: str
    major: str
    group: GroupType
    org_college: str


@dataclass
class Flight:
    uuid: UUID
    pilot: Pilot
    station_id: UUID
    valid: bool


@dataclass
class FlightPosition:
    flight: Flight
    ts: datetime
    x: float
    y: float
    z: float
    valid: bool = True
