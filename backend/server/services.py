from PIL import Image

from backend.blur_face.blurring import GaussianBlur, ImageBlur
from backend.blur_face.detection import Detector


class FaceBlurService:
   def __init__(self, blur_mask_fade=2, kernel_size=51, sigma=10):
       self._detector = Detector()
       blur_method = GaussianBlur(kernel_size, sigma)
       self._blurrer = ImageBlur(blur_method, blur_mask_fade)

   def blur_image(self, image):
       detected_faces = self._detector.detect(image)
       blurred_image_np = self._blurrer.blur(image, detected_faces)
       return Image.fromarray(blurred_image_np)