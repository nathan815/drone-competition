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


def get_cluster(cluster_ips_file: str = 'cluster_ips.txt') -> Cluster:
    auth = PlainTextAuthProvider(username=os.environ['DSE_USER'], password=os.environ['DSE_PASS'])
    with open(cluster_ips_file) as ips_file:
        ips = list(map(lambda ele: ele.strip(), ips_file.read().split(",")))
    logger.info(f'Read cluster nodes IPs from {cluster_ips_file}: {ips}')
    return Cluster(contact_points=ips, auth_provider=auth)


class CompetitionDatabase:
    def __init__(self, cluster: Cluster):
        self.session = cluster.connect('competition')
        self.insert_flight_data_stmt: Optional[PreparedStatement] = None

    def get_flights(self, limit: int = None) -> iter:
        cql = "select * from competition.positional"
        if limit:
            cql += f" limit {limit}"
        for row in self.session.execute(cql):
            yield Flight(
                row.flight_id,
                Pilot(row.name, row.major, row.group, row.org_college),
                row.station_id,
                row.valid
            )

    def create_flight(self, pilot: Pilot, station_id: uuid.UUID) -> Flight:
        uuid = uuid.uuid1()
        ts = datetime.now()
        flight = Flight(uuid, pilot, station_id, True)
        flight_pos = FlightPosition(flight, ts, 0, 0, 0)
        self.insert_flight_position(flight_pos)
        return flight

    def insert_flight_position(self, flight_position: FlightPosition):
        # prepare the statement once, then we don't have to send the entire query for every insertion
        if not self.insert_flight_data_stmt:
            cql = "insert into competition.positional (" \
                  " flight_id, ts, latest_ts, x, y, z, station_id," \
                  " name, major, org_college, group, num_crashes, valid" \
                  ") values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?)"
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
            flight_position.flight.pilot.group,
            flight_position.flight.valid
        ])


if __name__ == "__main__":
    db = CompetitionDatabase(get_cluster())
    print('All flights:')
    rows = db.get_flights()
    for r in rows:
        print(r)
