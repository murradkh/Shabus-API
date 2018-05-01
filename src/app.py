from src.Common.Database import Database
from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object('src.config')
app.secret_key = 'murrad'


#
@app.before_first_request
def ini_db():
    Database.init_Database()


@app.route('/', methods=['GET'])
def home():
    return "ok"


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=4990)
