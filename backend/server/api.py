import io

from PIL import Image
from flask import send_file
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage

from backend.server.services import FaceBlurService

IMAGE_FILE_NAME = 'image_file'


class BlurImage(Resource):
    def __init__(self):
        super().__init__()
        self._face_blur_service = FaceBlurService()
        self._request_parser  = reqparse.RequestParser()
        self._request_parser.add_argument(IMAGE_FILE_NAME, type=FileStorage, location='files')

    def post(self):
        args = self._request_parser.parse_args()
        image = Image.open(args[IMAGE_FILE_NAME])
        blurred_image = self._face_blur_service.blur_image(image)
        image_bytes = self._image_to_bytes(blurred_image)

        return send_file(image_bytes,
                         mimetype='image/jpeg',
                         as_attachment=True,
                         attachment_filename='blur.jpg')

    @staticmethod
    def _image_to_bytes(image):
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='JPEG')
        image_bytes.seek(0)
        return image_bytes


class BlurNSFW(Resource):
    ...
