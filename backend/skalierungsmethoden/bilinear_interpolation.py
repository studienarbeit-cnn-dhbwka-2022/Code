from backend.image import Image


class BilinearInterpolation(Image):
    def __init__(self, path):
        extend = "biLi"
        super().__init__(path, extend)

    def manipulate(self, new_size):
        super().manipulate(new_size)

        for y in range(self.new_height):
            for x in range(self.new_width):
                x_old = x / (self.new_width / self.width)
                y_old = y / (self.new_height / self.height)

                # Find the surrounding pixels
                x1 = int(x_old)
                x2 = min(x1 + 1, self.width - 1)
                y1 = int(y_old)
                y2 = min(y1 + 1, self.height - 1)

                # Find the weights
                w1 = (x2 - x_old) * (y2 - y_old)
                w2 = (x_old - x1) * (y2 - y_old)
                w3 = (x2 - x_old) * (y_old - y1)
                w4 = (x_old - x1) * (y_old - y1)

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
                self.newImg.putpixel((x, y), new_pixel)

        return self.save()
