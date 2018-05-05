from src.Common.Database import Database
from flask import Flask, render_template, url_for
import os
from src.models.users.views import Driver_blueprint

app = Flask(__name__)
app.config.from_object('src.config')

@app.before_first_request
def ini_db():
    Database.init_Database()

@app.route('/')
def home():

    return 'ok'


app.register_blueprint(Driver_blueprint, url_prefix='/users')
