import os

import pymongo


class Database(object):
    URI = None
    database = None

    @staticmethod
    def init_Database():
        Database.URI = os.environ.get('MONGODB_URI')
        client = pymongo.MongoClient(Database.URI)
        Database.database = client.get_database()

    @staticmethod
    def save_to_db(collection, query):
        Database.database[collection].insert(query)

    @staticmethod
    def find(collection, query,
             options=None):  # the option variable representing which field we want back from the DB. if not specified then return all the fields of required document
        return Database.database[collection].find(query, options)

    @staticmethod
    def find_one(collection, query, options=None):
        return Database.database[collection].find_one(query, options)

    @staticmethod
    def update(collection, query, update, upsert):
        Database.database[collection].update(query, {"$set": update}, upsert=upsert)

    @staticmethod
    def set_ttl_for_collection(collection, index_field,
                               expire_after_seconds):  # this function setting ttl(time to live) in  the database, so the documents in this collection will be deleted after the specified ttl
        try:
            Database.database.command('collMod', collection,
                                      index={'keyPattern': {index_field: 1},
                                             'background': True,
                                             'expireAfterSeconds': expire_after_seconds})
        except:  # thats in case the index is not set yet in the collection
            Database.database[collection].ensure_index(index_field, expireAfterSeconds=expire_after_seconds)
