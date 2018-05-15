import pymongo
from pymongo import Connection
from pymongo.dbref import DBRef
from pymongo.database import Database

# connect
connection = Connection()
db = Database(connection, "things")
