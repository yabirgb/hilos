import os
from peewee import *

DB_NAME = os.environ.get("DBNAME", None)
DB_USER = os.environ.get("DBUSER", None)
DB_PASS = os.environ.get("DBPASS", None)
DB_HOST = os.environ.get("DBHOST", None)

def calldb():
    db = PostgresqlDatabase(
        DB_NAME,  # Required by Peewee.
        user=DB_USER,  # Will be passed directly to psycopg2.
        password=DB_PASS,  # Ditto.
        host=DB_HOST,  # Ditto.
    )
    db.connect()
    return db

db = calldb()

class Branch(Model):
    height = IntegerField()

    class Meta:
        database = db

class Tweet(Model):
    date = DateField()
    reply_to = CharField(null=True)
    username = CharField()
    tweet_id = CharField(null=True)
    branch = ForeignKeyField(Branch, related_name="tweets")

    class Meta:
        database = db


class Tag(Model):
    branch = ForeignKeyField(Branch)
