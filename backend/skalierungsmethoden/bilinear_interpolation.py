from backend.image import Image
from PIL import Image as PILImage


class BilinearInterpolation(Image):
    def __init__(self, path):
        extend = "biLi"
        super().__init__(path, extend)

    def manipulate(self, new_size):
        if not new_size:
            new_size = (0, 0)
        width, height = self.img.size
        new_width, new_height = new_size if new_size != (0, 0) else (width * 2, height * 2)
        new_image = PILImage.new(self.img.mode, (new_width, new_height))

        for y in range(new_height):
            for x in range(new_width):
                x_old = x / (new_width / width)
                y_old = y / (new_height / height)

                # Find the surrounding pixels
                x1 = int(x_old)
                x2 = min(x1 + 1, width - 1)
                y1 = int(y_old)
                y2 = min(y1 + 1, height - 1)

                # Find the weights
                w1 = (x2 - x_old) * (y2 - y_old)
                w2 = (x_old - x1) * (y2 - y_old)
                w3 = (x2 - x_old) * (y_old - y1)
                w4 = (x_old - x1) * (y_old - y1)

                # Normalize the weights
                w_sum = w1 + w2 + w3 + w4
                w1 /= w_sum
                w2 /= w_sum
                w3 /= w_sum
                w4 /= w_sum

                # Get the pixel values of the surrounding pixels
                p1 = self.img.getpixel((x1, y1))
                p2 = self.img.getpixel((x2, y1))
                p3 = self.img.getpixel((x1, y2))
                p4 = self.img.getpixel((x2, y2))

                # Interpolate the pixel value
                new_pixel = (
                    int(w1 * p1[0] + w2 * p2[0] + w3 * p3[0] + w4 * p4[0]),
                    int(w1 * p1[1] + w2 * p2[1] + w3 * p3[1] + w4 * p4[1]),
                    int(w1 * p1[2] + w2 * p2[2] + w3 * p3[2] + w4 * p4[2])
                )
                new_image.putpixel((x, y), new_pixel)

        self.newImg = new_image

        return self.save()
