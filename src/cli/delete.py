import sys
from ..core.database import get_cluster, CompetitionDatabase

flight_id_arg = sys.argv[1] if len(sys.argv) > 1 else None

db = CompetitionDatabase(get_cluster())

flight = None

if flight_id_arg:
    flight_id = flight_id_arg
    flight = db.get_flight(flight_id)
else:
    flight = db.get_most_recent_flight()

answer = input(f"Are you sure you want to delete the flight${flight.uuid} by {flight.pilot.name} {flight.pilot.group} {flight.pilot.major}? y/n")

if answer.upper() == 'Y' and flight:
    print("Deleting flight...")
    db.delete_flight(flight.uuid)
    print("Flight DELETED!")
else:
    print("Did not delete deleted")
