import cv2
import numpy as np

def histogram_equalization(frame, clahe=False, clip_limit=2.0, tile_grid=(8,8)):
    """
    Apply global or adaptive histogram equalization.
    :param frame: input image (BGR or grayscale)
    :param clahe: whether to apply CLAHE
    :param clip_limit: CLAHE clip limit
    :param tile_grid: CLAHE grid size
    :return: equalized image
    """
    if frame is None:
        raise ValueError("Input frame is None")
    
    gray = frame
    if len(frame.shape) == 3:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    if clahe:
        clahe_obj = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid)
        eq_img = clahe_obj.apply(gray)
    else:
        eq_img = cv2.equalizeHist(gray)
    
    return eq_img

def process_image():
    img = cv2.imread('image.jpg', cv2.IMREAD_UNCHANGED)
    if img is None:
        print('Error: Image not found.')
        return
    
    # Apply both global and CLAHE
    out_global = histogram_equalization(img, clahe=False)
    out_clahe = histogram_equalization(img, clahe=True)
    
    cv2.imwrite('output_hist_eq_global.jpg', out_global)
    cv2.imwrite('output_hist_eq_clahe.jpg', out_clahe)

if __name__ == '__main__':
    process_image()
