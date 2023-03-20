from backend.image import Image
from PIL import Image as PILImage
import math


class LanczosInterpolation(Image):
    def __init__(self, path):
        extend = "lcz"
        super().__init__(path, extend)

    def lanczos_kernel(self, x, a=2):
        if x == 0:
            return 1
        elif abs(x) >= a:
            return 0
        else:
            return math.sin(math.pi * x) * math.sin(math.pi * x / a) / (math.pi ** 2 * x ** 2)

    def manipulate(self, new_size):
        if not new_size:
            new_size = (0, 0)
        width, height = self.img.size
        new_width, new_height = new_size if new_size != (0, 0) else (width * 2, height * 2)
        new_image = PILImage.new(self.img.mode, (new_width, new_height))

        # Lanczos interpolation
        # https://en.wikipedia.org/wiki/Lanczos_resampling

        for i in range(new_width):
            for j in range(new_height):
                # Calculate the corresponding coordinates in the original image
                x, y = i * width / new_width, j * height / new_height
                u, v = math.floor(x), math.floor(y)
                s, t = x - u, y - v

                # Interpolate the pixel value using a 5x5 kernel centered at the corresponding coordinates
                pixel = (0, 0, 0)
                weight_sum = 0

                for m in range(u - 2, u + 3):
                    for n in range(v - 2, v + 3):
                        if m >= 0 and n >= 0 and m < width and n < height:
                            weight = self.lanczos_kernel(s - (m - u)) * self.lanczos_kernel(t - (n - v))
                            pixel = tuple([p + weight * self.img.getpixel((m, n))[i] for i, p in enumerate(pixel)])
                            weight_sum += weight
                if weight_sum > 0:
                    pixel = tuple([int(p / weight_sum) for p in pixel])
                    new_image.putpixel((i, j), pixel)

        self.newImg = new_image

        return self.save()
