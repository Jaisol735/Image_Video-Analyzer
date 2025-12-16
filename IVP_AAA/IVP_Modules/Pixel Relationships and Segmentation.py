import cv2
import numpy as np
from skimage import measure

def pixel_segmentation(frame, connectivity=8, min_area=50):
    """
    Label connected components and extract region properties.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if len(frame.shape)==3 else frame
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    labels = measure.label(binary, connectivity=connectivity)
    props = measure.regionprops(labels)

    out = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
    for prop in props:
        if prop.area >= min_area:
            y0, x0, y1, x1 = prop.bbox
            cv2.rectangle(out, (x0, y0), (x1, y1), (0,255,0), 1)
    
    return labels, props

def process_image():
    img = cv2.imread('image.jpg')
    if img is None:
        print('Error: Image not found.')
        return
    
    labels, props = pixel_segmentation(img)
    # Render labels overlay for saving
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    out = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
    for prop in props:
        if prop.area >= 50:
            y0, x0, y1, x1 = prop.bbox
            cv2.rectangle(out, (x0, y0), (x1, y1), (0,255,0), 1)
    cv2.imwrite('output_pixel_segments.jpg', out)

if __name__ == '__main__':
    process_image()
