import os

DEBUG = True
ADMINS = {'murradkhalil@gmail.com', 'ibrahim.abu.rmaila@gmail.com'}
SECRET_KEY = os.environ["SESSION_SECRET_KEY"]
TOKEN_LIFETIME = os.environ['Shift_duration_In_hours']  # in hours
INDEX_FIELD_FOR_TTL = 'createdAt'
# ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
# AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
ACCOUNT_SID = '123'
AUTH_TOKEN = '123'
