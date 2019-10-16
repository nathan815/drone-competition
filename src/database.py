from dse import ConsistencyLevel
from dse.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from dse.policies import WhiteListRoundRobinPolicy, DowngradingConsistencyRetryPolicy
from dse.query import tuple_factory

profile = ExecutionProfile(WhiteListRoundRobinPolicy(['127.0.0.1']),
                           DowngradingConsistencyRetryPolicy(),
                           ConsistencyLevel.LOCAL_QUORUM,
                           ConsistencyLevel.LOCAL_SERIAL,
                           15, tuple_factory)
cluster = Cluster(['my-dse'])
session = cluster.connect()

print(session.execute("SELECT release_version FROM system.local")[0])
