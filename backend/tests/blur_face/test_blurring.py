import unittest
from unittest.mock import MagicMock, patch

import numpy as np

from backend.blur_face.blurring import ImageBlur


class TestImageBlur(unittest.TestCase):

    def test_init(self):
        _ = ImageBlur(MagicMock(), MagicMock(), MagicMock())

    @patch('numpy.array')
    def test_blur(self, np_array_mock):
        np_array_mock.return_value = np.zeros((10, 10, 3))
        blurring_algorithm_mock = MagicMock()
        image_blur = ImageBlur(blurring_algorithm_mock, MagicMock(), MagicMock())

        image = MagicMock()
        image_blur.blur(image, MagicMock())

        blurring_algorithm_mock.assert_called_once()
