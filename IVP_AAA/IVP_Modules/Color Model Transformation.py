import cv2
import numpy as np

def color_model_transform(frame):
    """
    Perform color slicing, remapping, and balance adjustment.
    """
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Color slicing example: keep only red tones
    lower_red = np.array([0,100,50])
    upper_red = np.array([10,255,255])
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    red_only = cv2.bitwise_and(frame, frame, mask=mask_red)

    # Histogram matching example (simplified)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_equalized = cv2.equalizeHist(gray)

    return {'Red_Slice':red_only, 'Gray_Equalized':gray_equalized}

def process_image():
    img = cv2.imread('image.jpg')
    if img is None:
        print('Error: Image not found.')
        return
    
    out = color_model_transform(img)
    cv2.imwrite('output_red_slice.jpg', out['Red_Slice'])
    cv2.imwrite('output_gray_equalized.jpg', out['Gray_Equalized'])

if __name__ == '__main__':
    process_image()
