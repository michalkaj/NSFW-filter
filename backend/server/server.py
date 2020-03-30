import base64
import io

from flask import Flask, request, send_file, jsonify
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
    image.save(image_bytes, format='PNG')
    # image_bytes.seek(0)
    img_str = base64.b64encode(image_bytes.getvalue())
    return img_str

def get_image(img):
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    encoded_img = base64.encodebytes(img_byte_arr.getvalue()).decode('ascii')
    return encoded_img

@app.route('/blur/<filename>', methods=['POST'])
def blur_image(filename):
    image_content = request.files['image_file']
    image = Image.open(image_content)
    blurred_image = _blur_image(image)
    image_bytes = get_image(blurred_image)
    return jsonify({'image': image_bytes})



@app.route('/nsfw/<filename>', methods=['POST'])
def nsfw_filter(filename):
    return f'Filename {filename}'


if __name__ == '__main__':
    app.run(debug=True, port=BACKEND_PORT)
