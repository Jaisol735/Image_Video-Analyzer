import cv2
import numpy as np
from sklearn.naive_bayes import GaussianNB

def bayesian_otsu(frame, sample_pixels=None):
    """
    Perform supervised Bayesian pixel classification (GaussianNB) and Otsu thresholding.
    :param sample_pixels: dict {label: list of [r,g,b]}
    """
    img = frame.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape)==3 else img

    # Otsu
    _, otsu_mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Bayesian
    if sample_pixels:
        X = []
        y = []
        for label, pixels in sample_pixels.items():
            X.extend(pixels)
            y.extend([label]*len(pixels))
        X = np.array(X); y = np.array(y)
        clf = GaussianNB()
        clf.fit(X, y)
        flat = img.reshape(-1, img.shape[2]) if len(img.shape)==3 else gray.reshape(-1,1)
        pred = clf.predict(flat)
        bayes_mask = pred.reshape(gray.shape)
    else:
        bayes_mask = None

    return otsu_mask, bayes_mask

def process_image():
    img = cv2.imread('image.jpg')
    if img is None:
        print('Error: Image not found.')
        return
    
    otsu, bayes = bayesian_otsu(img, sample_pixels=None)
    cv2.imwrite('output_otsu.jpg', otsu)
    if bayes is not None:
        # Normalize to 0-255 if labels are arbitrary
        bnorm = (255 * (bayes.astype(np.float32) - bayes.min()) / max(1, (bayes.max()-bayes.min()))).astype(np.uint8)
        cv2.imwrite('output_bayesian.jpg', bnorm)

if __name__ == '__main__':
    process_image()
