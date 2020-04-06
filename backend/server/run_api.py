from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from backend.server.api import BlurImage
from settings import BACKEND_PORT

app = Flask(__name__)
api = Api(app)
cors = CORS(app, support_credential=True)

api.add_resource(BlurImage, '/blur')
app.run(debug=True, port=BACKEND_PORT)
