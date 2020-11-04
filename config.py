import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# GIVE SQLALCHEMY URL
# SQLALCHEMY_DATABASE_URI = 'postgresql://cone_db_user:cone_db_user#123@localhost:5432/cone_db'
SQLALCHEMY_DATABASE_URI = 'postgres://wnewegyzucwobl:81f398918a2ead66f5c9b2d4829610c0312a0dcab6bf0c6cc7e5d27701c375d5@ec2-34-237-89-96.compute-1.amazonaws.com:5432/dfrari7q7ikdhv'
# SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

app = Flask(__name__)

app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


print('config.py', SQLALCHEMY_DATABASE_URI)
