from peewee import *
import peeweedbevolve

from models_data import Tweet, Branch, calldb

db = calldb()

def create_tables():
    calldb()
    db.evolve([Tweet, Branch])
    print("Tables created")


create_tables()
