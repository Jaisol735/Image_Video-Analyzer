import cv2
import numpy as np

def thresholding_intensity_slicing():
    img = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("Error: Image not found.")
        return

    # Define range as np arrays (not literals)
    lower_bound = np.array(100, dtype=np.uint8)
    upper_bound = np.array(200, dtype=np.uint8)

    mask = cv2.inRange(img, lower_bound, upper_bound)

    cv2.imwrite('output_intensity_slice.jpg', mask)

if __name__ == '__main__':
    thresholding_intensity_slicing()
