# distance_measures.py
import cv2
import numpy as np

def compute_image_distances():
    img1 = cv2.imread('image.jpg')
    if img1 is None:
        print("Error loading image.")
        return

    # For single image analysis, compute internal statistics
    gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY) if len(img1.shape) == 3 else img1
    
    # Compute pixel value statistics
    mean_val = np.mean(gray)
    std_val = np.std(gray)
    min_val = np.min(gray)
    max_val = np.max(gray)
    
    # Compute histogram
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    
    with open('output_distances.txt', 'w') as f:
        f.write(f"Image Statistics:\n")
        f.write(f"Mean Value: {mean_val:.2f}\n")
        f.write(f"Standard Deviation: {std_val:.2f}\n")
        f.write(f"Min Value: {min_val}\n")
        f.write(f"Max Value: {max_val}\n")
        f.write(f"Dynamic Range: {max_val - min_val}\n")
    
    # Save histogram as image
    hist_img = np.zeros((256, 256), dtype=np.uint8)
    hist_normalized = hist.ravel() / hist.max()
    for i in range(256):
        cv2.line(hist_img, (i, 255), (i, 255 - int(hist_normalized[i] * 255)), 255)
    cv2.imwrite('output_histogram.jpg', hist_img)

if __name__ == '__main__':
    compute_image_distances()
