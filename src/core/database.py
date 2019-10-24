import os
from dse.auth import PlainTextAuthProvider
from dse.cluster import Cluster

ap = PlainTextAuthProvider(username=os.environ['DSE_USER'], password=os.environ['DSE_PASS'])

ips_file = open('cluster_ips.txt')
ips = list(map(lambda ele: ele.strip(), ips_file.read().split(",")))
ips_file.close()
print('Cluster nodes IPs:', ips)

cluster = Cluster(ips, auth_provider=ap)
session = cluster.connect()

rows = session.execute("SELECT * FROM competition.positional")
for row in rows:
    print(row)
