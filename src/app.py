from datetime import timedelta

from src.Common.Database import Database
from flask import Flask, session
from src.models.users.views import Driver_blueprint

app = Flask(__name__)
app.config.from_object('src.config')
app.secret_key = app.config['SECRET_KEY']
app.permanent_session_lifetime = timedelta(hours= int(app.config['PERMANENT_SESSION_LIFETIME']))

@app.before_first_request
def ini_db():
    Database.init_Database()

@app.route('/')
def home():
    return 'ok'


app.register_blueprint(Driver_blueprint, url_prefix='/users')
