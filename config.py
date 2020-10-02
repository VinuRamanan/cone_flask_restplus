import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# SQLALCHEMY_DATABASE_URI = ''  #GIVE SQLALCHEMY URL
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

app = Flask(__name__)

app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

print('config.py', SQLALCHEMY_DATABASE_URI)
