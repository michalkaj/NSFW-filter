import unittest
from unittest.mock import MagicMock, patch

from blur_face.detection import Detector


class TestDetector(unittest.TestCase):

    def test_init(self):
        _ = Detector()

    @patch('backend.blur_face.detection.MTCNN.detect')
    def test_detect(self, detect_mock):
        detect_mock.return_value = ([MagicMock()], MagicMock(), [MagicMock()])
        detector = Detector()
        image = MagicMock()

        with patch('backend.blur_face.detection.FaceBoundingBox'):
            detector.detect(image)

        detect_mock.assert_called_once()
