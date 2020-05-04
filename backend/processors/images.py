import uuid
from os import remove

from PIL.Image import Image, fromarray

from blur_face.blurring import PixelBlur, GaussianBlur, ImageBlur
from blur_face.detection import Detector
from nudenet import NudeClassifier
from blur_face.bounding_box import BoundingBox


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
        self._blur = ImageBlur(blur_method, blur_mask_fade)

    def __call__(self, image: Image) -> Image:
        detected_faces = self._detector.detect(image)
        blurred_image_np = self._blur.blur(image, detected_faces)
        return fromarray(blurred_image_np)


class CensorNudity:
    def __init__(self, blur_mask_fade=2, kernel_size=101, sigma=16):
        self._classifier = NudeClassifier()
        self._labels_of_acceptable = ['BELLY', 'M_BREAST']
        blur_method = PixelBlur(30)
        self._blur = ImageBlur(blur_method, blur_mask_fade)

    def __call__(self, image: Image) -> Image:
        path = str(uuid.uuid4()) + '.jpg'
        Image.save(image, path)
        detected_nudity = self._classifier.classify(path)
        remove(path)
        if detected_nudity[path]['unsafe'] > 0.7:
            nudity_boxes = [BoundingBox(0, 0, image.size[0], image.size[1])]
            blurred_image_np = self._blur.blur(image, nudity_boxes)
            return fromarray(blurred_image_np)
        else:
            return image


