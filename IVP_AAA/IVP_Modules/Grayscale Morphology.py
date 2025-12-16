import cv2
import numpy as np

def grayscale_morphology(frame, operation='gradient', kernel_size=3):
    """
    Apply morphological operations on grayscale image: gradient, tophat, blackhat.
    :param frame: grayscale image
    :param operation: 'gradient', 'tophat', 'blackhat'
    :param kernel_size: structuring element size
    :return: processed image
    """
    if frame is None:
        raise ValueError("Input frame is None")
    
    gray = frame
    if len(frame.shape) == 3:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    
    if operation == 'gradient':
        result = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, kernel)
    elif operation == 'tophat':
        result = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, kernel)
    elif operation == 'blackhat':
        result = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)
    else:
        raise ValueError("Operation must be 'gradient', 'tophat', or 'blackhat'")
    
    return result

def process_image():
    img = cv2.imread('image.jpg', cv2.IMREAD_UNCHANGED)
    if img is None:
        print('Error: Image not found.')
        return
    
    out_g = grayscale_morphology(img, operation='gradient', kernel_size=3)
    out_t = grayscale_morphology(img, operation='tophat', kernel_size=3)
    out_b = grayscale_morphology(img, operation='blackhat', kernel_size=3)
    cv2.imwrite('output_gray_gradient.jpg', out_g)
    cv2.imwrite('output_gray_tophat.jpg', out_t)
    cv2.imwrite('output_gray_blackhat.jpg', out_b)

if __name__ == '__main__':
    process_image()
