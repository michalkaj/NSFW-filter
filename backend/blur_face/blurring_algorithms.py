import cv2
import numpy as np
from PIL import Image


class GaussianBlur:
    def __init__(self, kernel_size=3, sigma=1):
        self.kernel_size = kernel_size
        self.sigma = sigma

    def __call__(self, image):
        image = np.array(image)
        return cv2.GaussianBlur(
            image,
            (self.kernel_size, self.kernel_size),
            self.sigma
        )


class PixelBlur:
    def __init__(self, shrinkage_factor):
        self.shrinkage_factor = shrinkage_factor

    def __call__(self, image):
        small_size = (int(image.size[0] / self.shrinkage_factor),
                      int(image.size[1] / self.shrinkage_factor))
        image_small = image.resize(small_size, resample=Image.BILINEAR)
        return image_small.resize(image.size, Image.NEAREST)