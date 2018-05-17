import os

import pymongo


class Database(object):
    URI = None
    database = None

    @staticmethod
    def init_Database():
        Database.URI = os.environ.get('MONGODB_URI')
        client = pymongo.MongoClient(Database.URI)
        Database.database = client.get_default_database()

    @staticmethod
    def save_to_db(collection, query):
        Database.database[collection].insert(query)

    @staticmethod
    def find(collection, query):
        return Database.database[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.database[collection].find_one(query)

    @staticmethod
    def update(collection, query, update, upsert):
        Database.database[collection].update(query, update, upsert=upsert)

    @staticmethod
    def set_ttl_for_collection(collection, index_field,
                               expire_after_seconds):  # this function setting ttl(time to live) in  the database, so the documents in this collection will be deleted after the specified ttl
        Database.database[collection].ensure_index(index_field, expireAfterSeconds=expire_after_seconds)
