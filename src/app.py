from flask import Flask

from src.Common.Database import Database
from src.config import TOKEN_LIFETIME
from src.models.User.Driver.constants import Index_field_for_ttl, DB_collection_current_driver_shift
from src.models.User.Driver.views import Driver_blueprint
from src.models.User.Passenger.views import passenger_blueprint

app = Flask(__name__)
app.config.from_object('src.config')
app.secret_key = app.config['SECRET_KEY']


# app.permanent_session_lifetime = timedelta(hours= int(app.config['PERMANENT_SESSION_LIFETIME']))

@app.before_first_request
def ini_db():
    Database.init_Database()
    Database.set_ttl_for_collection(DB_collection_current_driver_shift, index_field=Index_field_for_ttl,
                                    expire_after_seconds=int(TOKEN_LIFETIME) * 60 * 60)


@app.route('/')
def home():
    return 'ok'


app.register_blueprint(Driver_blueprint, url_prefix='/User/Driver')
app.register_blueprint(passenger_blueprint, url_prefix='/User/Passenger')
