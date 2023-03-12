def pixel_verdopplung(image):
import numpy as np
import cv2

def pixel_doubling(image, scale_factor):
    new_size = (int(image.shape[1] * scale_factor), int(image.shape[0] * scale_factor))
    
    scaled_image = np.zeros(new_size + (image.shape[2],), dtype=np.uint8)
    for i in range(new_size[0]):
        for j in range(new_size[1]):
            x = int(i / scale_factor)
            y = int(j / scale_factor)
            scaled_image[j, i] = image[y, x]
    
    return scaled_image

image = cv2.imread('cactus.jpg')
scaled_image = pixel_doubling(image, 2)
cv2.imshow(scaled_image)
    pass
