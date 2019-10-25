// Run this CQL on a node in the cluster

CREATE KEYSPACE competition
    WITH replication = {'class':'SimpleStrategy', 'replication_factor':3};

USE competition;

CREATE TABLE positional
(
    flight_id   TIMEUUID,
    ts          TIMESTAMP,
    x           DOUBLE,
    y           DOUBLE,
    z           DOUBLE,
    latest_ts   TIMESTAMP STATIC,
    station_id  UUID STATIC,
    num_crashes INT STATIC,
    name        TEXT STATIC,
    group       TEXT STATIC,
    org_college TEXT STATIC,
    major       TEXT STATIC,
    valid       BOOLEAN STATIC,
    PRIMARY KEY (flight_id, ts)
) WITH CLUSTERING ORDER BY (ts DESC);
