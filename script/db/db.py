from pymongo import MongoClient


def connect_db(db_name):
    client = MongoClient('localhost', 27017)
    db = client[db_name]
    return db
