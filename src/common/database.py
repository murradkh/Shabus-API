import os

import pymongo
from gridfs import GridFS

from src.common.errors import DBErrors


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
        try:
            data = Database.database[collection].insert(query)
            if data is None:
                raise Exception
            return data
        except Exception:
            DBErrors("failed in saving the data, maybe because the data already exist!")

    @staticmethod
    def find(collection, query,
             options=None):  # the option variable representing which field we want back from the DB. if not specified then return all the fields of required document
        data = Database.database[collection].find(query, options)
        if data is None:
            raise DBErrors("the data not found in db")
        return data

    @staticmethod
    def find_one(collection, query, options=None):
        data = Database.database[collection].find_one(query, options)
        if data is None:
            raise DBErrors("the data not found in db")
        return data

    @staticmethod
    def find_one_and_delete(collection, query, options=None):
        data = Database.database[collection].find_one_and_delete(query, options)
        if data is None:
            raise DBErrors("the data not found in db")
        return data

    @staticmethod
    def update(collection, query, update, upsert=False):
        data = Database.database[collection].update(query, {"$set": update}, upsert=upsert)
        if data is None:
            raise DBErrors("can't update the documents in db")
        return data

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

    @staticmethod
    def find_image(collection, filter):
        fs = GridFS(Database.database, collection=collection)
        image = fs.find_one(filter=filter)
        if image is None:
            raise DBErrors("the image not found!")
        return image

    @staticmethod
    def save_image(collection, image_details, image):
        fs = GridFS(Database.database, collection=collection)
        image_fs = fs.new_file(**image_details)
        image_fs.write(image.encode())
        image_fs.close()

    @staticmethod
    def delete_image(collection, filter):
        fs = GridFS(Database.database, collection=collection)
        image_grid_out = fs.find_one(filter)
        if image_grid_out is None:
            raise DBErrors("the image not found!")
        fs.delete(image_grid_out._id)

    @staticmethod
    def delete(collection, filter):
        data = Database.database[collection].remove(filter)
        if data is None:
            raise DBErrors("the data not found in db")
        return data
