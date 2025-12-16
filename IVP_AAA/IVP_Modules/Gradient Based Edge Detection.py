import cv2
import numpy as np

def gradient_edge_detection(frame, method='sobel'):
    """
    Compute image gradient magnitude and direction.
    :param frame: grayscale or BGR image
    :param method: 'sobel' or 'prewitt'
    :return: gradient magnitude and direction
    """
    if frame is None:
        raise ValueError("Input frame is None")
    
    gray = frame
    if len(frame.shape) == 3:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    if method == 'sobel':
        gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    elif method == 'prewitt':
        kernelx = np.array([[1,0,-1],[1,0,-1],[1,0,-1]])
        kernely = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
        gx = cv2.filter2D(gray, cv2.CV_64F, kernelx)
        gy = cv2.filter2D(gray, cv2.CV_64F, kernely)
    else:
        raise ValueError("Method must be 'sobel' or 'prewitt'")
    
    magnitude = cv2.magnitude(gx, gy)
    direction = cv2.phase(gx, gy, angleInDegrees=True)
    
    return magnitude, direction

def process_image():
    img = cv2.imread('image.jpg')
    if img is None:
        print('Error: Image not found.')
        return
    
    mag, ang = gradient_edge_detection(img, method='sobel')
    cv2.imwrite('output_grad_mag.jpg', cv2.convertScaleAbs(mag))

if __name__ == '__main__':
    process_image()
