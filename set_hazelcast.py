import json
from consul import Consul

cl = Consul()
cl.kv.put("queue_name", json.dumps("queue"))
cl.kv.put("map_name", json.dumps("my-distributed-map1"))
