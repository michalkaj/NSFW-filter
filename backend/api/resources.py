import io

from PIL import Image
from flask import send_file
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage

from processors.images import Ensure3Channels, EnsureImageSize, BlurFaces
from processors.pipeline import Pipeline

IMAGE_FILE_NAME = 'image_file'
MAX_IMAGE_SIZE = 1000


class BlurImageResource(Resource):
    def __init__(self):
        super().__init__()
        self._face_blur_pipeline = self._init_pipeline()
        self._request_parser  = reqparse.RequestParser()
        self._request_parser.add_argument(IMAGE_FILE_NAME, type=FileStorage, location='files')

    def post(self):
        args = self._request_parser.parse_args()
        image = Image.open(args[IMAGE_FILE_NAME])
        blurred_image = self._face_blur_pipeline.apply(image)
        image_bytes = self._image_to_bytes(blurred_image)

        return send_file(image_bytes,
                         mimetype='image/jpeg',
                         as_attachment=True,
                         attachment_filename='blur.jpg')

    def _init_pipeline(self):
        pipeline = Pipeline()
        pipeline.add_step(Ensure3Channels())
        pipeline.add_step(EnsureImageSize(MAX_IMAGE_SIZE, MAX_IMAGE_SIZE))
        pipeline.add_step(BlurFaces())
        return pipeline

    @staticmethod
    def _image_to_bytes(image):
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='JPEG')
        image_bytes.seek(0)
        return image_bytes


class BlurNSFW(Resource):
    ...
