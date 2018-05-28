from flask import Flask

from src.Common.Database import Database
from src.models.User.Driver.views import Driver_blueprint
from src.models.User.Passenger.views import passenger_blueprint

app = Flask(__name__)
app.config.from_object('src.config')
app.secret_key = app.config['SECRET_KEY']


# app.permanent_session_lifetime = timedelta(hours= int(app.config['PERMANENT_SESSION_LIFETIME']))

@app.before_first_request
def ini_db():
    Database.init_Database()
    # Database.set_ttl_for_collection('Previous shifts', index_field="createdAt",
    #                                 expire_after_seconds=30*24 * 60 * 60)  # this command is run every time our server is waked up, i did this(instead of just one time to run the command)  for making our application dynamic, so in case the manager changed the expiration duration shift, it will work here.
    # Database.set_ttl_for_collection("New rides", index_field="createdAt",
    #                                 expire_after_seconds=30*24 * 60 * 60)  # this command is run every time our server is waked up, i did this(instead of just one time to run the command)  for making our application dynamic, so in case the manager changed the expiration duration shift, it will work here.
    #
    # Database.set_ttl_for_collection("Current shifts", index_field="createdAt",
    #                                 expire_after_seconds=30 * 24 * 60 * 60)  # this command is run every time our server is waked up, i did this(instead of just one time to run the command)  for making our application dynamic, so in case the manager changed the expiration duration shift, it will work here.



@app.route('/')
def home():
    return 'ok'


app.register_blueprint(Driver_blueprint, url_prefix='/User/Driver')
app.register_blueprint(passenger_blueprint, url_prefix='/User/Passenger')
