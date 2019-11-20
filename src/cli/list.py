from ..core.database import get_cluster, CompetitionDatabase

db = CompetitionDatabase(get_cluster())
flights = list(db.get_flights(10))

flights.reverse()

for flight in flights:
    print(flight)