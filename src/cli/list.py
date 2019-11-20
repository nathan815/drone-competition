from ..core.database import get_cluster, CompetitionDatabase

db = CompetitionDatabase(get_cluster())
flights = db.get_flights(10)

for flight in flights.reverse():
    print(flight)