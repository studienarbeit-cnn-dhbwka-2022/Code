from backend.image import Image
from PIL import Image as PILImage


class PixelVerdopplung(Image):
    def __init__(self, path):
        super().__init__(path, extend="p2")

    def manipulate(self, new_size=(0, 0)):
        width, height = self.img.size
        new_width, new_height = new_size if new_size != (0, 0) else (width * 2, height * 2)
        new_image = PILImage.new(self.img.mode, (new_width, new_height))

        for y in range(new_height):
            for x in range(new_width):
                x_old = int(x / (new_width / width))
                y_old = int(y / (new_height / height))
                old_pixel = self.img.getpixel((x_old, y_old))
                new_image.putpixel((x, y), old_pixel)

        return self.save()

