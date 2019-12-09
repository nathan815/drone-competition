from ..core.database import get_cluster, CompetitionDatabase

db = CompetitionDatabase(get_cluster())
flights = db.get_recent_flights(10)

flights.reverse()

for flight in flights:
    print(flight)
