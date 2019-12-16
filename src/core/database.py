import logging
import os
import time
from datetime import datetime
from typing import Optional
import uuid

from dse.auth import PlainTextAuthProvider
from dse.cluster import Cluster
from dse.query import PreparedStatement
from dse.util import uuid_from_time

from .model import FlightPosition, Flight, Pilot

logger = logging.getLogger(__name__)


def get_cluster(cluster_ips_file: str = 'ips.txt') -> Cluster:
    auth = PlainTextAuthProvider(username=os.environ['DSE_USER'], password=os.environ['DSE_PASS'])
    with open(cluster_ips_file) as ips_file:
        ips = list(map(lambda ele: ele.strip(), ips_file.read().split(",")))
    logger.info(f'Read cluster nodes IPs from {cluster_ips_file}: {ips}')
    return Cluster(contact_points=ips, auth_provider=auth)


class CompetitionDatabase:
    def __init__(self, cluster: Cluster):
        self.session = cluster.connect('competition')
        self.insert_flight_data_stmt: Optional[PreparedStatement] = None

    def get_recent_flights(self, limit: int = None) -> list:
        cql = "select * from competition.positional group by flight_id"
        flights = []
        for row in self.session.execute(cql):
            flights.append(Flight(
                row.flight_id,
                Pilot(row.name, row.major, row.group, row.org_college),
                row.station_id,
                row.valid
            ))
        flights.sort(key=lambda flight: flight.latest_ts, reverse=True)
        if limit:
            flights = flights[:limit]
        return flights

    def get_flight(self, flight_id: uuid.UUID):
        stmt = self.session.prepare("select * from competition.positional where flight_id = ? group by flight_id")
        the_row = None
        for row in self.session.execute(stmt, [flight_id]):
            the_row = row
        print(the_row)
        if the_row:
            return Flight(the_row.flight_id, Pilot(the_row.name, the_row.major, the_row.group, the_row.org_college), the_row.station_id, the_row.valid)

    def get_most_recent_flight(self) -> Flight:
        return self.get_recent_flights(1)[0]

    def delete_flight(self, flight_id):
        stmt = self.session.prepare("delete from competition.positional where flight_id = ?")
        self.session.execute(stmt, [flight_id])

    def insert_new_flight(self, flight: Flight) -> Flight:
        ts = datetime.utcnow()
        flight_pos = FlightPosition(flight, ts, 0, 0, 0)
        self.insert_flight_position(flight_pos)
        return flight

    def insert_flight_position(self, flight_position: FlightPosition):
        # prepare the statement once, then we don't have to send the entire query for every insertion
        if not self.insert_flight_data_stmt:
            cql = "insert into competition.positional (" \
                  " flight_id, ts, latest_ts, x, y, z, station_id," \
                  " name, major, org_college, group, num_crashes" \
                  ") values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)"
            self.insert_flight_data_stmt = self.session.prepare(cql)

        return self.session.execute(self.insert_flight_data_stmt, [
            flight_position.flight.uuid,
            flight_position.ts,
            flight_position.ts,
            flight_position.x,
            flight_position.y,
            flight_position.z,
            flight_position.flight.station_id,
            flight_position.flight.pilot.name,
            flight_position.flight.pilot.major,
            flight_position.flight.pilot.org_college,
            flight_position.flight.pilot.group
        ])

    def set_flight_invalid_ttl(self, flight_id):
        stmt = self.session.prepare("UPDATE positional USING TTL 25 SET valid=false WHERE flight_id = ?")
        self.session.execute(stmt, [flight_id])

    def set_flight_valid(self, flight_id):
        stmt = self.session.prepare("UPDATE positional SET valid=true WHERE flight_id = ?")
        self.session.execute(stmt, [flight_id])


if __name__ == "__main__":
    db = CompetitionDatabase(get_cluster())
    print('All flights:')
    rows = db.get_recent_flights()
    for r in rows:
        print(r)
