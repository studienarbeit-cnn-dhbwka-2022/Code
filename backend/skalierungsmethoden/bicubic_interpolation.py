import math

from backend.image import Image


def _cubic(x, a=-0.5):
    abs_x = abs(x)
    if abs_x <= 1:
        return (a + 2) * (abs_x ** 3) - (a + 3) * (abs_x ** 2) + 1
    elif abs_x < 2:
        return a * (abs_x ** 3) - (5 * a) * (abs_x ** 2) + (8 * a) * abs_x - (4 * a)
    return 0


def _get_weight(distance):
    # calculate the weight for the given distance
    abs_distance = abs(distance)
    if abs_distance <= 1:
        return _cubic(abs_distance)
    return 0


class BicubicInterpolation(Image):
    def __init__(self, path):
        extend = "biCu"
        super().__init__(path, extend)

    def manipulate(self, new_size):
        super().manipulate(new_size)

        # iterate over each pixel in the new image
        for y in range(self.new_height):
            for x in range(self.new_width):
                # calculate the corresponding pixel coordinates in the original image
                px = x * self.width / self.new_width
                py = y * self.height / self.new_height

                # calculate the integer coordinates of the surrounding pixels in the original image
                ix = math.floor(px)
                iy = math.floor(py)

                # calculate the fractional distance of the current pixel from the surrounding pixels
                dx = px - ix
                dy = py - iy

                # calculate the weights for each of the surrounding pixels
                weights = []
                for j in range(-1, 3):
                    for i in range(-1, 3):
                        weight = _get_weight(i - dx) * _get_weight(dy - j)
                        weights.append(weight)

                # normalize the weights
                total_weight = sum(weights)
                normalized_weights = [w / total_weight for w in weights]

                # calculate the new pixel value
                new_pixel = [0, 0, 0]
                for j in range(-1, 3):
                    for i in range(-1, 3):
                        # get the pixel value from the original image
                        ox = ix + i
                        oy = iy + j
                        if ox < 0 or oy < 0 or ox >= self.width or oy >= self.height:
                            # if the pixel is outside the original image, use black
                            pixel_value = [0, 0, 0]
                        else:
                            pixel_value = list(self.img.getpixel((ox, oy)))

                        # add the weighted pixel value to the new pixel
                        weight_index = (j + 1) * 4 + (i + 1)
                        weight = normalized_weights[weight_index]
                        for k in range(3):
                            new_pixel[k] += weight * pixel_value[k]

                # set the new pixel value in the new image
                self.newImg.putpixel((x, y), (int(new_pixel[0]), int(new_pixel[1]), int(new_pixel[2])))

        return self.save()

