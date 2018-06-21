import os

DEBUG = True
ADMINS = {'murradkhalil@gmail.com', 'ibrahim.abu.rmaila@gmail.com'}
SECRET_KEY = os.environ["SESSION_SECRET_KEY"]
TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
PHONE_NUMBER = "Shabus"
