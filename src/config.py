import os

DEBUG = True
ADMINS = set(['murradkhalil@gmail.com','ibrahim.abu.rmaila@gmail.com'])
SECRET_KEY = os.environ["SESSION_SECRET_KEY"]
TOKEN_LIFETIME = os.environ['TOKEN_LIFETIME_InHours']  # in hours
