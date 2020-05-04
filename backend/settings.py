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

NUDITY_DETECTION_SETTINGS = {
    'blur_mask_fade': 2,
    'threshold': 0.6
}

try:
    from user_settings import * # silence pyflakes
except ImportError:
    pass
