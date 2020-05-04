from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from api.resources import BlurImageResource
from api.resources import BlurNSFW
from processors.pipeline import get_blur_nsfw_pipeline, get_blur_face_pipeline
from settings import BACKEND_PORT

_MAX_IMAGE_SIZE = 1000

app = Flask(__name__)
api = Api(app)
cors = CORS(app, support_credential=True)

api.add_resource(
    BlurImageResource,
    '/blur',
    resource_class_kwargs={'pipeline': get_blur_face_pipeline(_MAX_IMAGE_SIZE)}
)
api.add_resource(
    BlurNSFW,
    '/nsfw',
    resource_class_kwargs={'pipeline': get_blur_nsfw_pipeline(_MAX_IMAGE_SIZE)}
)

app.run(debug=True, port=BACKEND_PORT, use_reloader=False)
