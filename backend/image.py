from PIL import Image as PILImage
import os


class Image:
    def __init__(self, path, extend):
        self.path = path
        self.newPath = os.path.join(os.path.dirname(path), f"{extend}_{os.path.basename(path)}")
        self.img = PILImage.open(path)

    def manipulate(self, new_size):
        pass

    def save(self):
        try:
            self.img.save(self.newPath)
            return self.newPath
        except:
            return "./img/ALAAARM.png"
