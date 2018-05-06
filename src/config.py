import os

DEBUG = True
ADMINS = set(['murradkhalil@gmail.com','ibrahim.abu.rmaila@gmail.com'])
SECRET_KEY = os.environ["SESSION_SECRET_KEY"]
PERMANENT_SESSION_LIFETIME = os.environ['PERMANENT_SESSION_LIFETIME']  # in hours
