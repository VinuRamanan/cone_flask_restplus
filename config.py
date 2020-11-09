import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json


print(os.listdir())
with open('C:\\yarn_application\\settings.json', 'r') as f:
    settings = json.load(f)


# GIVE SQLALCHEMY URL
SQLALCHEMY_DATABASE_URI = settings['SQLALCHEMY_URI']

app = Flask(__name__)

app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
