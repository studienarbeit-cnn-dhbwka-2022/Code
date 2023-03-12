def nearest_neighbour(image):
import numpy as np
import cv2

def nearest_neighbor_interpolation(image, scale_factor):
    new_size = (int(image.shape[1] * scale_factor), int(image.shape[0] * scale_factor))
    
    scaled_image = np.zeros(new_size + (image.shape[2],), dtype=np.uint8)
    for i in range(new_size[0]):
        for j in range(new_size[1]):
            x = int(i / scale_factor)
            y = int(j / scale_factor)
            scaled_image[j, i] = image[y, x]
    
    return scaled_image


image = cv2.imread('example_image.jpg')
scaled_image = nearest_neighbor_interpolation(image, 2)
cv2.imshow(image)
cv2.imshow(scaled_image)
    pass
