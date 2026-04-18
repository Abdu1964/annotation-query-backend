import os
import traceback
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

    client = MongoClient(uri)
    try:
        try:
            db = client.get_default_database()
        except Exception:
            db = client.test

        schemas = {
            "annotation": Annotation(empty=True).schema,
            "user": User(empty=True).schema,
            "shared_annotation": SharedAnnotation(empty=True).schema,
        }

        set_schemas(db, schemas)

        mongo_db = db
        logging.info("MongoDB Connected!")
        return db
        
    except Exception as e:
        traceback.print_exc()
        logging.error(f"Error initializing database {e}")
        raise RuntimeError(f"Error initializing database {e}")