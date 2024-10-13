from pymongo.mongo_client import MongoClient
from pymongo.database import Database
from os.path import join, dirname
from typing import Optional
import os
from dotenv import load_dotenv

def signleTon(class_instance):
    instances = {}
    
    def get_instances(*args, **kwargs):
        if class_instance not in instances:
            instances[class_instance] = class_instance(*args, **kwargs)
        return instances[class_instance]
    
    return get_instances

@signleTon
class MongoDBConnection:
    
    def __init__(self, url_database, db_connection):
        self._client = MongoClient(url_database)
        self._db = self._client[db_connection]
    
    def get_database(self) -> Database:
        return self._db

# mongodb connection manager
dotenv_path = os.path.join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

uri = os.environ.get("MONGODB_URL")
database_name = os.environ.get("DATABASE_NAME")
# object connect to database
connection_manager = MongoDBConnection(uri, database_name)


def get_database():
    # create database
    database = connection_manager.get_database()
    return database