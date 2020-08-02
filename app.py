from apis import api
from flask_cors import CORS
from config import app

CORS(app)

api.init_app(app)
app.run(debug=True)
