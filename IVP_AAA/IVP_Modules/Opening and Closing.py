import cv2
import numpy as np

def opening_closing(frame, kernel_size=3, operation='opening'):
    """
    Apply morphological opening (erosion→dilation) or closing (dilation→erosion).
    :param frame: input binary or grayscale image
    :param kernel_size: structuring element size
    :param operation: 'opening' or 'closing'
    :return: processed image
    """
    if frame is None:
        raise ValueError("Input frame is None")
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    
    if operation == 'opening':
        result = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
    elif operation == 'closing':
        result = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel)
    else:
        raise ValueError("Operation must be 'opening' or 'closing'")
    
    return result

def process_image():
    img = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)
    if img is None:
        print('Error: Image not found.')
        return
    
    out_o = opening_closing(img, kernel_size=3, operation='opening')
    out_c = opening_closing(img, kernel_size=3, operation='closing')
    cv2.imwrite('output_opening.jpg', out_o)
    cv2.imwrite('output_closing.jpg', out_c)

if __name__ == '__main__':
    process_image()
