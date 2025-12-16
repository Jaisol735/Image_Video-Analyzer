import cv2
import numpy as np

def color_histogram(frame, ref_frame=None):
    """
    Compute per-channel histograms, apply CLAHE, and optional histogram matching.
    """
    b,g,r = cv2.split(frame)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    r_clahe = clahe.apply(r)
    g_clahe = clahe.apply(g)
    b_clahe = clahe.apply(b)
    clahe_img = cv2.merge([b_clahe,g_clahe,r_clahe])

    return {'CLAHE_Image':clahe_img}

def process_image():
    img = cv2.imread('image.jpg')
    if img is None:
        print('Error: Image not found.')
        return
    
    out = color_histogram(img)
    cv2.imwrite('output_color_clahe.jpg', out['CLAHE_Image'])

if __name__ == '__main__':
    process_image()
