from typing import Iterable

import torch
from PIL.Image import Image
from facenet_pytorch import MTCNN

from blur_face.bounding_box import FaceBoundingBox
from settings import FACE_DETECTION_SETTINGS


class Detector:
    def __init__(self):
        device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self._model = MTCNN(device=device, **FACE_DETECTION_SETTINGS)

    def detect(self, image: Image) -> Iterable[FaceBoundingBox]:
        boxes, _, points = self._model.detect(image, landmarks=True)
        if boxes is not None:
            return [self._array_to_bbox(a, p) for a, p in zip(boxes, points)]
        else:
            return []

    @staticmethod
    def _array_to_bbox(array_bbox, points):
        return FaceBoundingBox(array_bbox[:2], array_bbox[2:], *points)
