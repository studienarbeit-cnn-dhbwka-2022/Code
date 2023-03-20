from backend.image import Image


def _cubic(x, a=-0.5):
    abs_x = abs(x)
    if abs_x <= 1:
        return (a + 2) * (abs_x ** 3) - (a + 3) * (abs_x ** 2) + 1
    elif abs_x < 2:
        return a * (abs_x ** 3) - (5 * a) * (abs_x ** 2) + (8 * a) * abs_x - (4 * a)
    return 0


class BicubicInterpolation(Image):
    def __init__(self, path):
        extend = "biCu"
        super().__init__(path, extend)

    def manipulate(self, new_size):
        super().manipulate(new_size)

        for y in range(self.new_height):
            for x in range(self.new_width):
                x_old = x / (self.new_width / self.width)
                y_old = y / (self.new_height / self.height)

                # Find the surrounding pixels
                x1 = int(x_old) - 1
                x2 = x1 + 1
                x3 = x2 + 1
                x4 = x3 + 1
                y1 = int(y_old) - 1
                y2 = y1 + 1
                y3 = y2 + 1
                y4 = y3 + 1

                # Find the fractional part of the x and y coordinates
                frac_x = x_old - int(x_old)
                frac_y = y_old - int(y_old)

                # Calculate the coefficients
                cx = [_cubic(i - frac_x) for i in range(4)]
                cy = [_cubic(i - frac_y) for i in range(4)]

                # Get the pixel values of the surrounding pixels
                pixels = []
                for j in range(y1, y4 + 1):
                    row_pixels = []
                    for i in range(x1, x4 + 1):
                        try:
                            row_pixels.append(self.img.getpixel((i, j)))
                        except IndexError:
                            pass
                    pixels.append(row_pixels)

                # Interpolate the pixel value
                red = 0
                green = 0
                blue = 0
                for i in range(4):
                    for j in range(4):
                        try:
                            red += cx[i] * cy[j] * pixels[j][i][0]
                            green += cx[i] * cy[j] * pixels[j][i][1]
                            blue += cx[i] * cy[j] * pixels[j][i][2]
                        except IndexError:
                            pass

                new_pixel = (
                    int(max(0, min(255, red))),
                    int(max(0, min(255, green))),
                    int(max(0, min(255, blue)))
                )
                self.newImg.putpixel((x, y), new_pixel)

        return self.save()
