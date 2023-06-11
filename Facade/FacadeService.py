import random

import uvicorn
from fastapi import FastAPI, APIRouter
import requests
import json
from pydantic import BaseModel

class Item(BaseModel):
    id:int
    content : str


class StartItem(BaseModel):
    content : str

class FacadeService():
    def __init__(self):
        self.indeces = set()
    async def get_from_logging(self, url):
        x = requests.get(url)

        return x


    async def get_from_messages(self, url):
        x = requests.get(url)

        return x
    async def post_to_messages(self, item,url):
        msg = Item(id=0, content=item.content)
        msg1 = msg.json()

        json_object = json.loads(msg1)
        x = requests.post(url, json=json_object)

    async def post_to_logging(self, start_msg:StartItem, url):

        uuid = random.randint(0,1000000)
        while uuid in self.indeces:
            uuid = random.randint(0, 1000000)
        self.indeces.add(uuid)
        msg = Item(id=uuid, content=start_msg.content)


        url_log = url
        msg1 = msg.json()


        json_object = json.loads(msg1)
        x = requests.post(url_log, json=json_object)
        return x
