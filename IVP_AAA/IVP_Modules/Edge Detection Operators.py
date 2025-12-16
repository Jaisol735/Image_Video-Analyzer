import cv2
import numpy as np

def edge_detection_operators(frame):
    """
    Apply classic edge detection operators: Prewitt, Sobel, Laplacian, LoG, and Canny.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if len(frame.shape)==3 else frame

    # Sobel
    sobel = cv2.Sobel(gray, cv2.CV_64F, 1, 1, ksize=3)
    sobel = cv2.convertScaleAbs(sobel)

    # Prewitt
    kernelx = np.array([[1,0,-1],[1,0,-1],[1,0,-1]])
    kernely = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
    prewitt = cv2.filter2D(gray, -1, kernelx) + cv2.filter2D(gray, -1, kernely)

    # Laplacian
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    laplacian = cv2.convertScaleAbs(laplacian)

    # LoG (Laplacian of Gaussian)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    log = cv2.Laplacian(blur, cv2.CV_64F)
    log = cv2.convertScaleAbs(log)

    # Canny
    v = np.median(gray)
    lower = int(max(0, 0.66*v))
    upper = int(min(255, 1.33*v))
    canny = cv2.Canny(gray, lower, upper)

    return {'sobel':sobel, 'prewitt':prewitt, 'laplacian':laplacian, 'log':log, 'canny':canny}

def process_image():
    img = cv2.imread('image.jpg')
    if img is None:
        print('Error: Image not found.')
        return
    
    out = edge_detection_operators(img)
    cv2.imwrite('output_sobel.jpg', out['sobel'])
    cv2.imwrite('output_prewitt.jpg', out['prewitt'])
    cv2.imwrite('output_laplacian.jpg', out['laplacian'])
    cv2.imwrite('output_log.jpg', out['log'])
    cv2.imwrite('output_canny.jpg', out['canny'])

if __name__ == '__main__':
    process_image()
