from typing import Callable, List

from PIL.Image import Image

from processors.images import Ensure3Channels, EnsureImageSize, BlurFaces, CensorNudity


class Pipeline:
    def __init__(self, steps: List[Callable[[Image], Image]]=None):
        self._steps = steps or []

    def add_step(self, processor: Callable[[Image], Image]):
        self._steps.append(processor)

    def apply(self, image: Image) -> Image:
        for processor in self._steps:
            image = processor(image)
        return image


def get_blur_face_pipeline(max_image_size):
    pipeline = Pipeline()
    pipeline.add_step(Ensure3Channels())
    pipeline.add_step(EnsureImageSize(max_image_size, max_image_size))
    pipeline.add_step(BlurFaces())
    return pipeline


def get_blur_nsfw_pipeline(max_image_size):
    pipeline = Pipeline()
    pipeline.add_step(Ensure3Channels())
    pipeline.add_step(EnsureImageSize(max_image_size, max_image_size))
    pipeline.add_step(CensorNudity())
    return pipeline