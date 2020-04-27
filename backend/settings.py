import os

PROJECT_PATH = os.path.dirname(__file__)
DATA_PATH = None
BACKEND_PORT = 2137

FACE_DETECTION_SETTINGS = {
    'image_size': 160,
    'margin': 0,
    'min_face_size': 12,
    'thresholds': [0.5, 0.65, 0.65],
    'factor': 0.9,
    'post_process': True,
    'keep_all': True,
    'select_largest': False
}

try:
    from user_settings import * # silence pyflakes
except ImportError:
    pass
