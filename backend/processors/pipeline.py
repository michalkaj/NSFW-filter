from typing import Callable, List

from PIL.Image import Image


class Pipeline:
    def __init__(self, steps: List[Callable[[Image], Image]]=None):
        self._steps = steps or []

    def add_step(self, processor: Callable[[Image], Image]):
        self._steps.append(processor)

    def apply(self, image: Image) -> Image:
        for processor in self._steps:
            image = processor(image)
        return image
