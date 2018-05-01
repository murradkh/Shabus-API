import flask_bcrypt
import bcrypt
import  os
import pymongo
import uuid

class Database(object):
    # URI = os.environ.get('MONGODB_URI')
    URI = 'mongodb://murrad:123@ds263619.mlab.com:63619/heroku_7k387d67'
    database = None

    @staticmethod
    def init_Database():
        client = pymongo.MongoClient(Database.URI)
        Database.database = client.get_default_database()

    @staticmethod
    def save_to_DB(collection, query):
        Database.database[collection].insert(query)

    @staticmethod
    def find(collection, query):
        Database.database[collection].find_one(query)

    @staticmethod
    def find_one(collection, query):
        Database.database[collection].find(query)

    @staticmethod
    def update(collection, query, data):
        Database.database[collection].update(query, data, upsert=True)

    @staticmethod
    def remove(collection, query, just_one):
        Database.database[collection].remove(collection, query, just_one)








# Database.init_Database()
#
# hashed_password = bcrypt.hashpw(b"123",bcrypt.gensalt())
# email = 'murradkhalil@gmail.com'
# D = {'_id': uuid.uuid4().hex, 'email':email, 'Password': hashed_password.decode()}
# Database.save_to_DB('Drivers', D)


# import psycopg2 as p

# try:
#     connection = p.connect("dbname='d2ink2ug7q191f' user='ewvctvrtnsgwwc' host='ec2-54-228-251-254.eu-west-1.compute.amazonaws.com' password='35b1b3c3129277497c85646ebd99cdf2edecc490cd03b4cb0532656d7fbfd962' port='5432'")
#     connection.autocommit = True
#     cursor = connection.cursor()
# except:
#     print("Cannot connect to database")
#
# cursor = connection.cursor()
# create_table_command = 'select * from user_'
# cursor.execute(create_table_command)
# data = list(cursor.fetchall())
#
# create_table_command = 'select * from  roles_users'
# cursor.execute(create_table_command)
# roles_users = cursor.fetchall()
# Drivers_id = []
# for i in roles_users:
#     if i[1] == 2:
#         Drivers_id.append(i)
#
#
# Drivers_details = [(i[0],i[1],i[2]) for i in data if (i[0],2) in Drivers_id ]
#
# create_table_command = 'select * from  passenger'
# cursor.execute(create_table_command)
# passengers = cursor.fetchall()
#
#
# # [Database.save_to_DB("Drivers", {'_id': i[0], 'email':i[1], 'Password':i[2]}) for i in Drivers_details]
# [Database.save_to_DB("Passengers", {'_id': i[0], 'member_id': i[1], 'passenger_type': str(i[2]), 'id_number': i[6], 'phone_number': i[5], 'name':((str(i[3])+" "+str(i[4])) if i[4] is not None else 'None'), 'has_smartphone': str(i[7])}) for i in passengers]
#
