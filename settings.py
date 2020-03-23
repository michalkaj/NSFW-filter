import os

PROJECT_PATH = os.path.dirname(__file__)
DATA_PATH = None

FACE_DETECTION_SETTINGS = {
    'image_size': 160,
    'margin': 0,
    'min_face_size': 20,
    'thresholds': [0.6, 0.7, 0.7],
    'factor': 0.709,
    'post_process': True,
    'keep_all': True
}

try:
    from user_settings import * # silence pyflakes
except:
    ImportError
