import cv2
import numpy as np
from PIL import Image

from blur_face.bounding_box import FaceBoundingBox


class ImageBlur:
    def __init__(self, blur_algorithm, blur_mask_fade, landmark_eps=0.1):
        self.blur_algorithm = blur_algorithm
        self.blur_mask_fade = blur_mask_fade
        self.landmark_eps = landmark_eps

    def blur(self, image, bounding_boxes):
        image_arr = np.array(image)

        image_arr_blurred = np.array(self.blur_algorithm(image))

        mask = self._get_blur_mask(image_arr.shape, bounding_boxes)
        mask_multidim = mask[..., None].repeat(3, axis=2)
        final_image_arr = image_arr * (1 - mask_multidim) + image_arr_blurred * mask_multidim
        return final_image_arr.clip(0, 255).astype(np.uint8)

    def _get_blur_mask(self, shape, bounding_boxes):
        mask = np.zeros(shape[:2], dtype=np.float64)

        mesh_x, mesh_y = self._get_mesh(shape)
        for box in bounding_boxes:
            center = box.center
            sigma_x = box.width / self.blur_mask_fade
            sigma_y = box.height / self.blur_mask_fade
            if isinstance(box, FaceBoundingBox):
                self._hard_blur_face(mask, box)
            delta_mask = self._gauss2d(mesh_x, mesh_y, (center.x, center.y), (sigma_x, sigma_y))
            mask += delta_mask

        return mask.clip(0, 1)

    def _hard_blur_face(self, mask, face):
        from_x = face.left_eye.x - int(face.width * self.landmark_eps)
        to_x = face.right_eye.x + int(face.width * self.landmark_eps)
        from_y = face.left_eye.y - int(face.height * self.landmark_eps)
        to_y = face.left_eye.y + int(face.height * self.landmark_eps)
        mask[from_y: to_y,
             from_x: to_x] = 1

    @staticmethod
    def _get_mesh(shape):
        xs = np.linspace(0, shape[0], shape[0])
        ys = np.linspace(0, shape[1], shape[1])
        return np.meshgrid(ys, xs)

    @staticmethod
    def _gauss2d(x, y, mu, sigma):
        mx, my = mu
        sx, sy = sigma
        exp = np.exp(-((x - mx)**2. / (2. * sx**2.) + (y - my)**2. / (2. * sy**2.)))
        denom = (2. * np.pi * sx * sy)
        z = 1. / denom * exp
        z /= z.max()
        return z


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
