import cv2
import numpy as np

def digital_image_representation():
    img = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("Error: Image not found.")
        return

    img = img.astype(np.float32)  # ensure correct dtype
    mean_val = np.mean(img)
    std_val = np.std(img)

    # Save a small text report instead of printing
    with open('output_image_stats.txt', 'w') as f:
        f.write(f"Mean Intensity: {mean_val:.2f}\n")
        f.write(f"Standard Deviation: {std_val:.2f}\n")

if __name__ == '__main__':
    digital_image_representation()
