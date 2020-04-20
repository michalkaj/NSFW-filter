from PIL.Image import Image, fromarray

from backend.blur_face.blurring import GaussianBlur, ImageBlur
from backend.blur_face.detection import Detector


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
