import unittest
from unittest.mock import MagicMock

from backend.processors.pipeline import Pipeline


class TestPipeline(unittest.TestCase):

    def test_init(self):
        _ = Pipeline()

    def test_apply(self):
        pipeline = Pipeline()

        mocks = [MagicMock() for _ in range(10)]
        for mock in mocks:
            pipeline.add_step(mock)

        pipeline.apply(MagicMock())

        for mock in mocks:
            mock.assert_called_once()
