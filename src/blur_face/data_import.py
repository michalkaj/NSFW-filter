import os
import os.path

from PIL import Image


class DataImport:
    images = []
    path = "images"
    valid_images = [".jpg", ".gif", ".png", ".tga"]

    def import_images(self):
        self.images = []
        for f in os.listdir(self.path):
            ext = os.path.splitext(f)[1]
            if ext.lower() not in self.valid_images:
                print("Wrong file format")
            self.images.append(Image.open(os.path.join(self.path, f)))
        return self.images

    def _get_images(self):
        return self.images

    def _set_path(self, path):
        self.path = path
