import random
import hazelcast
from fastapi import FastAPI, APIRouter
from FacadeService import FacadeService
from pydantic import BaseModel
import random
from asyncio import Lock
from fastapi import HTTPException

import uvicorn
from fastapi import FastAPI, APIRouter

from pydantic import BaseModel

from FacadeService import FacadeService

import json
from consul import Consul, Check




cl = Consul()
fc_name = "facade"
lg_name = "log"
ms_name = "message"

index, queue_name_data = cl.kv.get("queue_name")
index, map_name_data = cl.kv.get("map_name")

queue_name = json.loads(queue_name_data['Value'].decode('utf-8'))
map_name = json.loads(map_name_data['Value'].decode('utf-8'))

client = hazelcast.HazelcastClient()
queue = client.get_queue(queue_name)

class Item(BaseModel):
    content: str
    id: int


class StartItem(BaseModel):
    content: str


class FacadeController():

    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/", self.get_request, methods=["GET"])
        self.router.add_api_route("/", self.post_request, methods=["POST"])
        self.fs = FacadeService()
        self.lock = Lock()

    async def get_request(self):
        print(f"Received get in facade...")


        services = cl.health.service(lg_name, passing=True)[1]
        log_urls = []
        for service in services:
            address = service['Service']['Address']
            port = service['Service']['Port']
            log_url = f"http://{address}:{port}"

            log_urls.append(log_url)

        log_url = random.choice(log_urls)
        r = await self.fs.get_from_logging(log_url)
        print(r.text)



        services = cl.health.service(ms_name, passing=True)[1]
        ms_urls = []
        ports = []
        for service in services:
            # service = services[0]
            address = service['Service']['Address']
            port = service['Service']['Port']
            ports.append(port)
            ms_url = f"http://{address}:{port}"

            ms_urls.append(ms_url)

        ms_url = random.choice(ms_urls)

        out = ""
        for i in range(len(ms_urls)):
            r1 = await self.fs.get_from_messages(ms_urls[i])
            out += r1.text
            out += " "
        print("From messages:")
        print(out)

        return 0

    async def post_request(self, item: StartItem):
        queue.offer(item.json())


        print(f"Received post: \"{item.content}\" in facade...")

        services = cl.health.service(lg_name, passing=True)[1]
        log_urls = []
        for service in services:
            address = service['Service']['Address']
            port = service['Service']['Port']
            log_url = f"http://{address}:{port}"

            log_urls.append(log_url)

        log_url = random.choice(log_urls)
        r = await self.fs.post_to_logging(item, log_url)
        print(r.status_code)
        if r.status_code != 200:
            print("Something went wrong.")



        services = cl.health.service(ms_name, passing=True)[1]
        ms_urls = []
        ports = []
        for service in services:
            address = service['Service']['Address']
            port = service['Service']['Port']
            ports.append(port)
            ms_url = f"http://{address}:{port}"

            ms_urls.append(ms_url)

        ms_url = random.choice(ms_urls)

        r1 = await self.fs.post_to_messages(item, ms_url)

        return item.content


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='A test program.')

    parser.add_argument("--port", help="Prints the supplied argument.", default="A random string.")

    args = parser.parse_args()

    facade_port = int(args.port)

    fc_name = "facade"
    localhost = "127.0.0.1"

    cl.agent.service.register(service_id=f"facade:{facade_port}", name=fc_name, \
                                         address=localhost, port=facade_port, \
                                         check=Check.tcp(host=localhost, port=facade_port, interval=1, deregister=10))
    app = FastAPI()
    fc = FacadeController()
    app.include_router(fc.router)
    uvicorn.run(app, host=localhost, port=facade_port)
