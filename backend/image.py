from PIL import Image as PILImage
import os


class Image:
    def __init__(self, path, extend):
        self.path = path
        self.extend = extend
        self.img = PILImage.open(path)
        self.newName = f"{extend}_{os.path.basename(path)}"
        self.newPath = os.path.join(os.path.dirname(path), self.newName)
        self.newImg = None

    def manipulate(self, new_size):
        pass

    def save(self):
        try:
            if not self.newImg:
                Exception("No image to save")
            self.newImg.save(self.newPath)
            return self.newName
        except:
            return "ALAAARM.png"
