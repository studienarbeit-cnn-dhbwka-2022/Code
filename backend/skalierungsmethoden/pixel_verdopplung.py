from backend.image import Image


class PixelVerdopplung(Image):
    def __init__(self, path):
        extend = "p2"
        super().__init__(path, extend)

    def manipulate(self, new_size):
        super().manipulate(new_size)

        for y in range(self.new_height):
            for x in range(self.new_width):
                x_old = int(x / (self.new_width / self.width))
                y_old = int(y / (self.new_height / self.height))

                # Check that x_old and y_old are within bounds of original image
                if x_old >= self.width:
                    x_old = self.width - 1
                if y_old >= self.height:
                    y_old = self.height - 1

                old_pixel = self.img.getpixel((x_old, y_old))
                self.newImg.putpixel((x, y), old_pixel)

        return self.save()

