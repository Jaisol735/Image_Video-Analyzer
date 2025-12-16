import cv2
import numpy as np

def dilation_erosion(frame, kernel_size=3, operation='dilate'):
    """
    Apply morphological dilation or erosion.
    :param frame: input binary or grayscale image
    :param kernel_size: structuring element size
    :param operation: 'dilate' or 'erode'
    :return: processed image
    """
    if frame is None:
        raise ValueError("Input frame is None")
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size,kernel_size))
    if operation == 'dilate':
        result = cv2.dilate(frame, kernel, iterations=1)
    elif operation == 'erode':
        result = cv2.erode(frame, kernel, iterations=1)
    else:
        raise ValueError("Operation must be 'dilate' or 'erode'")
    
    return result

def process_image():
    img = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)
    if img is None:
        print('Error: Image not found.')
        return
    
    out_d = dilation_erosion(img, kernel_size=3, operation='dilate')
    out_e = dilation_erosion(img, kernel_size=3, operation='erode')
    cv2.imwrite('output_dilate.jpg', out_d)
    cv2.imwrite('output_erode.jpg', out_e)

if __name__ == '__main__':
    process_image()
