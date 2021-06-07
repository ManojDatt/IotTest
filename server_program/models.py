# -*- coding: utf-8 -*-
from pydantic import BaseModel
from datetime import datetime
from typing import Any
from pymongo import MongoClient
import os, yaml
from urllib.parse import quote_plus

with open(os.path.join(os.getcwd() , 'config.yml'), 'r') as stream:
    settings = yaml.load(stream, yaml.SafeLoader)

if settings.get('MONGODB_USERNAME', False) and settings.get('MONGODB_PASSWORD', False):
    uri = "mongodb://%s:%s@%s" % (quote_plus(settings.get('MONGODB_USERNAME')), quote_plus(settings.get('MONGODB_PASSWORD')), settings.get('MONGODB_HOST', 'localhost'))
    mdbclient = MongoClient(uri)
else:
    mdbclient = MongoClient(host=settings.get('MONGODB_HOST', 'localhost'), port=settings.get('MONGODB_PORT'))

DB = mdbclient.sensordb

class ResponseModel(BaseModel):
    code: int
    message: str
    error: str
    data: Any

class RequestModel(BaseModel):
    timestamp: datetime = "2020-12-03T11:48:43+05:30"
    sensor: str = "Sensor-2"
    value: float = 37.62
    

def serializeDict(a):
    return {**{i:str(a[i]) for i in a if i=='_id'},**{i:a[i] for i in a if i!='_id'}}

def serializeList(entity):
    return [serializeDict(a) for a in entity] 

def get_all_data(limit, offset):
    entity = DB.sensore_collection.find().limit(limit).skip(offset)
    return serializeList(entity)

def insert_data(data):
    entity = DB.sensore_collection.insert_one(data)
    obj = DB.sensore_collection.find_one({"_id": entity.inserted_id})
    return serializeDict(obj)