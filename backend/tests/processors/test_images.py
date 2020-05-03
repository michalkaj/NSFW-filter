import unittest
from unittest.mock import MagicMock, patch

import numpy as np
from PIL.Image import fromarray

from processors.images import BlurFaces, Ensure3Channels, EnsureImageSize


class TestEnsure3Channels(unittest.TestCase):

    def test_call_rgb(self):
        image_np = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        image = fromarray(image_np)

        image_processed = Ensure3Channels()(image)

        image_processed_np = np.array(image_processed)
        self.assertEqual(image_processed_np.shape[2], 3)

    def test_call_rgba(self):
        image_np = np.random.randint(0, 255, (224, 224, 4), dtype=np.uint8)
        image = fromarray(image_np)

        image_processed = Ensure3Channels()(image)

        image_processed_np = np.array(image_processed)
        self.assertEqual(image_processed_np.shape[2], 3)

class TestEnsureImageSize(unittest.TestCase):

    def test_call_smaller(self):
        image_np = np.random.randint(0, 255, (100, 500), dtype=np.uint8)
        image = fromarray(image_np)

        image_processed = EnsureImageSize(max_width=1000, max_height=1000)(image)

        self.assertEqual(
            image_processed.size,
            (500, 100)
        )

    def test_call_large(self):
        shape = (1000, 500, 3)
        image_np = np.random.randint(0, 255, shape, dtype=np.uint8)
        image = fromarray(image_np)

        image_processed = EnsureImageSize(max_width=100, max_height=100)(image)

        self.assertEqual(
            image_processed.size,
            (50, 100)
        )


class TestBlurFace(unittest.TestCase):
    def test_init(self):
        _ = BlurFaces()

    @patch('backend.processors.images.ImageBlur.blur')
    @patch('backend.processors.images.Detector.detect')
    def test_call(self, detect_mock, blur_mock):
        image = MagicMock()

        with patch('backend.processors.images.fromarray'):
            BlurFaces()(image)

        blur_mock.assert_called_once()
        detect_mock.assert_called_once()
