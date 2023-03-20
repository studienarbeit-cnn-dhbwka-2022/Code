from backend.image import Image
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
        super().manipulate(new_size)

        for i in range(self.new_width):
            for j in range(self.new_height):
                # Calculate the corresponding coordinates in the original image
                x, y = i * self.width / self.new_width, j * self.height / self.new_height
                u, v = math.floor(x), math.floor(y)
                s, t = x - u, y - v

                # Interpolate the pixel value using a 5x5 kernel centered at the corresponding coordinates
                pixel = (0, 0, 0)
                weight_sum = 0

                for m in range(u - 2, u + 3):
                    for n in range(v - 2, v + 3):
                        if 0 <= m < self.width and 0 <= n < self.height:
                            weight = self.lanczos_kernel(s - (m - u)) * self.lanczos_kernel(t - (n - v))
                            pixel = tuple([p + weight * self.img.getpixel((m, n))[i] for i, p in enumerate(pixel)])
                            weight_sum += weight
                if weight_sum > 0:
                    pixel = tuple([int(p / weight_sum) for p in pixel])
                    self.newImg.putpixel((i, j), pixel)

        return self.save()
