

from db import SessionLocal

# db connection 

import db_models
from db import SessionLocal, engine

db_models.Base.metadata.create_all(bind=engine)     #This line creates the tables in the database based on the models defined in db_models.py. It uses the metadata from the Base class to create the necessary tables in the database if they do not already exist.


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()