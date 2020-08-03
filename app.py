from apis import api
from flask_cors import CORS
from config import app
import os

CORS(app)

api.init_app(app)
