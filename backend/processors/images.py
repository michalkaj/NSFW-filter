import uuid
from pathlib import Path

import tensorflow as tf
from PIL.Image import Image, fromarray
from nudenet import NudeClassifier
from settings import NUDITY_DETECTION_SETTINGS

from blur_face.blurring import ImageBlur, FaceBlur
from blur_face.blurring_algorithms import GaussianBlur, PixelBlur
from blur_face.bounding_box import BoundingBox
from blur_face.detection import Detector


class Ensure3Channels:
    def __call__(self, image: Image) -> Image:
        return image.convert('RGB')


class EnsureImageSize:
    def __init__(self, max_width=1000, max_height=1000):
        self._max_width = max_width
        self._max_height = max_height

    def __call__(self, image: Image) -> Image:
        image = image.copy()
        image.thumbnail((self._max_width, self._max_height))
        return image


class BlurFaces:
    def __init__(self, blur_mask_fade=2, kernel_size=51, sigma=10):
        self._detector = Detector()
        blur_method = GaussianBlur(kernel_size, sigma)
        self._blur = FaceBlur(blur_method, blur_mask_fade)

    def __call__(self, image: Image) -> Image:
        detected_faces = self._detector.detect(image)
        blurred_image_np = self._blur.blur(image, detected_faces)
        return fromarray(blurred_image_np)


class CensorNudity:
    def __init__(self, blur_mask_fade=NUDITY_DETECTION_SETTINGS['blur_mask_fade'], threshold=NUDITY_DETECTION_SETTINGS['threshold']):
        self._classifier = NudeClassifier()
        self._blur = ImageBlur(PixelBlur(30), blur_mask_fade)
        self._threshold = threshold
        self._graph = tf.get_default_graph()

    def __call__(self, image: Image) -> Image:
        # Create temporary file (nudenet needs image to be saved)
        path = Path(str(uuid.uuid4()) + '.jpg')
        Image.save(image, path)

        with self._graph.as_default():
            detected_nudity = self._classifier.classify([path])

        # Delete temporary file
        path.unlink()

        if detected_nudity[path]['unsafe'] > self._threshold:
            nudity_boxes = [BoundingBox(0, 0, *image.size)]
            blurred_image_np = self._blur.blur(image, nudity_boxes)
            return fromarray(blurred_image_np)
        else:
            return image


