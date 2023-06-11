

import uvicorn
from fastapi import FastAPI, APIRouter
from LoggingRepository import  LoggingRepository
from pydantic import BaseModel


class Item(BaseModel):
    id:int
    content : str

class LoggingService():
    def __init__(self):
        self.lr = LoggingRepository()
    def addMessage(self,msg:Item):
        self.lr.addToMap(msg)
    def getLogs(self):
        return self.lr.getLogsFromMap()
