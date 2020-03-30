from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return 'This is index page'


@app.route('/blur/<filename>', methods=['POST'])
def blurImage(filename):
    if request.method == 'POST':
        return blurFunc(filename)
    else:
        return showPage()


@app.route('/nsfw/<filename>', methods=['POST'])
def nsfwFilter(filename):
    return f'Filename {filename}'


def blurFunc(filename):
    return f'Blurring {filename}'


def showPage():
    return 'Upland here'

if __name__ == '__main__':
    app.run(debug=True, port=2137)


