# image_transforms.py
import numpy as np
import cv2
from scipy.linalg import hadamard

def image_transforms(frame):
    """
    Apply DFT and Hadamard transform.
    :param frame: input image (grayscale)
    :return: dft_image, hadamard_image
    """
    if frame is None:
        raise ValueError("Input frame is None")
    
    gray = frame
    if len(frame.shape) == 3:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # DFT
    dft = np.fft.fft2(gray)
    dft_shift = np.fft.fftshift(dft)
    dft_image = np.log1p(np.abs(dft_shift))
    
    # Hadamard (requires size power of 2)
    N = 1 << (gray.shape[0]-1).bit_length()
    M = 1 << (gray.shape[1]-1).bit_length()
    padded = np.zeros((N,M))
    padded[:gray.shape[0], :gray.shape[1]] = gray
    H_N = hadamard(N)
    H_M = hadamard(M)
    hadamard_image = H_N @ padded @ H_M
    
    return dft_image, hadamard_image

def process_image():
    img = cv2.imread('image.jpg')
    if img is None:
        print('Error: Image not found.')
        return
    
    dft_img, had_img = image_transforms(img)
    # Normalize for saving
    dft_norm = cv2.normalize(dft_img, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    had_norm = cv2.normalize(had_img, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    cv2.imwrite('output_dft.jpg', dft_norm)
    cv2.imwrite('output_hadamard.jpg', had_norm)

if __name__ == '__main__':
    process_image()