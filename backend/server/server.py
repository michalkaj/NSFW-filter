import io

from flask import Flask, request, send_file
from flask_cors import CORS
from PIL import Image

from backend.blur_face.blurring import GaussianBlur, ImageBlur
from backend.blur_face.detection import Detector
from settings import BACKEND_PORT

app = Flask(__name__)
cors = CORS(app)

detector = Detector()
blur_method = GaussianBlur(51, 10)
blurrer = ImageBlur(blur_method, 2)


@app.route('/')
def index():
    return 'This is index page'


def _blur_image(image):
    detected_faces = detector.detect(image)
    blurred_image_np = blurrer.blur(image, detected_faces)
    return Image.fromarray(blurred_image_np)


def _image_to_bytes(image):
    image_bytes = io.BytesIO()
    image.save(image_bytes, 'PNG')
    image_bytes.seek(0)
    return image_bytes


@app.route('/blur/<filename>', methods=['POST'])
def blur_image(filename):
    image_content = request.files['image_file']
    image = Image.open(image_content)
    blurred_image = _blur_image(image)
    image_bytes = _image_to_bytes(blurred_image)

    return send_file(image_bytes, mimetype='image/PNG')


@app.route('/nsfw/<filename>', methods=['POST'])
def nsfw_filter(filename):
    return f'Filename {filename}'


if __name__ == '__main__':
    app.run(debug=True, port=BACKEND_PORT)
