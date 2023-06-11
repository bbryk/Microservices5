

import uvicorn
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
import hazelcast

import json
from consul import Consul, Check

cl = Consul()
index, queue_name_data = cl.kv.get("queue_name")
index, map_name_data = cl.kv.get("map_name")

queue_name = json.loads(queue_name_data['Value'].decode('utf-8'))
map_name = json.loads(map_name_data['Value'].decode('utf-8'))

class Item(BaseModel):
    id:int
    content : str


class LoggingRepository():
    def __init__(self):
        self.hz = hazelcast.HazelcastClient()
        self.map = self.hz.get_map(map_name).blocking()
    def addToMap(self,msg:Item):
        self.map.put(msg.id, msg.content)
        print(self.map)


    def getLogsFromMap(self):
        return ", ".join(self.map.values())
