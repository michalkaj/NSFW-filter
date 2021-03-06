from typing import Tuple, Iterable

import numpy as np

from blur_face.bounding_box import FaceBoundingBox, BoundingBox


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

    def _get_blur_mask(self, shape: Tuple, bounding_boxes: Iterable[BoundingBox]):
        mask = np.zeros(shape[:2], dtype=np.float64)

        for box in bounding_boxes:
            mask[box.upper_left.y: box.lower_right.y, box.upper_left.x: box.lower_right.x] = 1.

        return mask


class FaceBlur(ImageBlur):
    def _get_blur_mask(self, shape: Tuple, bounding_boxes: Iterable[FaceBoundingBox]):
        mask = np.zeros(shape[:2], dtype=np.float64)

        mesh_x, mesh_y = self._get_mesh(shape)
        for box in bounding_boxes:
            center = box.center
            sigma_x = box.width / self.blur_mask_fade
            sigma_y = box.height / self.blur_mask_fade
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
