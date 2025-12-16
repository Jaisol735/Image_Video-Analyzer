import cv2
import numpy as np

def smoothing_spatial_filters():
    img = cv2.imread('image.jpg')
    if img is None:
        print("Error: Image not found.")
        return

    blur = cv2.blur(img, (5, 5))
    gaussian = cv2.GaussianBlur(img, (5, 5), 0)
    bilateral = cv2.bilateralFilter(img, 9, 75, 75)

    kernel = np.ones((5, 5), np.float32) / 25
    filter2d = cv2.filter2D(img, -1, kernel)

    cv2.imwrite('output_blur.jpg', blur)
    cv2.imwrite('output_gaussian.jpg', gaussian)
    cv2.imwrite('output_bilateral.jpg', bilateral)
    cv2.imwrite('output_filter2d.jpg', filter2d)

if __name__ == '__main__':
    smoothing_spatial_filters()
