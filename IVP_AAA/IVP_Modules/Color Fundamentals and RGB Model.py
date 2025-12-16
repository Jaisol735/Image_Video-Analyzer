import cv2
import numpy as np

def color_fundamentals(frame):
    """
    Demonstrate RGB channels, splitting/merging, and basic manipulations.
    """
    b,g,r = cv2.split(frame)
    merged = cv2.merge([b,g,r])

    # Channel scaling example
    r_scaled = cv2.convertScaleAbs(r, alpha=1.2, beta=0)

    return {'R':r, 'G':g, 'B':b, 'Merged':merged, 'R_scaled':r_scaled}

def process_image():
    img = cv2.imread('image.jpg')
    if img is None:
        print('Error: Image not found.')
        return
    
    out = color_fundamentals(img)
    cv2.imwrite('output_r.jpg', out['R'])
    cv2.imwrite('output_g.jpg', out['G'])
    cv2.imwrite('output_b.jpg', out['B'])
    cv2.imwrite('output_r_scaled.jpg', out['R_scaled'])

if __name__ == '__main__':
    process_image()
