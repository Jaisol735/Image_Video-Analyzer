import cv2
import numpy as np

def contrast_stretching():
    img = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("Error: Image not found.")
        return

    r1, r2 = float(np.min(img)), float(np.max(img))
    if r2 <= r1:
        stretched = img.copy()
    else:
        stretched = ((img.astype(np.float32) - r1) / (r2 - r1)) * 255.0
        stretched = np.clip(stretched, 0, 255).astype(np.uint8)

    cv2.imwrite('contrast_stretched.jpg', stretched)

if __name__ == '__main__':
    contrast_stretching()
