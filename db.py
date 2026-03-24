import os
import logging
from pymongo import MongoClient
from pymongoose.methods import set_schemas
from app.models.annotation import Annotation
from app.models.user import User
from app.models.shared_annotation import SharedAnnotation
from dotenv import load_dotenv

load_dotenv()
mongo_db = None

def mongo_init():
    global mongo_db
    
    uri = os.environ.get("MONGO_URI")
    if not uri:
        logging.error("MONGO_URI is not set.")
        raise RuntimeError("MONGO_URI is not set.")

    db_name = os.environ.get("MONGO_DB_NAME", "annotation")
    client = MongoClient(uri)
    db = client[db_name]
    try:
        # Define the shcemas

    _client = MongoClient(
        uri,
        maxPoolSize=20,
        connectTimeoutMS=5000,
    )

    _db = _client[db_name]

    schemas = {
        "annotation": Annotation(empty=True).schema,
        "user": User(empty=True).schema,
        "shared_annotation": SharedAnnotation(empty=True).schema,
    }

    set_schemas(_db, schemas)
    logging.info("MongoDB Connected!")

    return _db

def get_db():
    if _db is None:
        raise RuntimeError("MongoDB not initialized in this process")
    return _db
