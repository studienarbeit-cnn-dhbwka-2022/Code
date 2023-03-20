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
        self.new_height = None
        self.new_width = None
        self.height = None
        self.width = None

    def manipulate(self, new_size):
        if not new_size:
            new_size = (0, 0)
        self.width, self.height = self.img.size
        self.new_width, self.new_height = new_size if new_size != (0, 0) else (self.width * 2, self.height * 2)
        self.newImg = PILImage.new(self.img.mode, (self.new_width, self.new_height))

    def save(self):
        try:
            if not self.newImg:
                Exception("No image to save")
            self.newImg.save(self.newPath)
            return self.newName
        except:
            return "ALAAARM.png"
