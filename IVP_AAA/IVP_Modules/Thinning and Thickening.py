import cv2
import numpy as np
from skimage.morphology import skeletonize, dilation

def thinning_thickening(frame, operation='thinning'):
    """
    Perform skeletonization (thinning) or thickening on binary image.
    :param frame: binary image
    :param operation: 'thinning' or 'thickening'
    :return: processed image
    """
    if frame is None:
        raise ValueError("Input frame is None")
    
    binary = (frame > 127).astype(np.uint8)
    
    if operation == 'thinning':
        result = skeletonize(binary).astype(np.uint8)
    elif operation == 'thickening':
        result = dilation(binary).astype(np.uint8)
    else:
        raise ValueError("Operation must be 'thinning' or 'thickening'")
    
    return result * 255

def process_image():
    img = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)
    if img is None:
        print('Error: Image not found.')
        return
    
    out_t = thinning_thickening(img, operation='thinning')
    out_k = thinning_thickening(img, operation='thickening')
    cv2.imwrite('output_thinning.jpg', out_t)
    cv2.imwrite('output_thickening.jpg', out_k)

if __name__ == '__main__':
    process_image()
