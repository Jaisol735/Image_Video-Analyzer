import cv2
import numpy as np

def image_negative(image_path='image.jpg'):
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print("Error loading image.")
        return

    negative = 255 - img
    cv2.imwrite("output_negative.jpg", negative)

if __name__ == '__main__':
    image_negative()
