# discrete_cosine_transform.py
import cv2
import numpy as np

def block_dct(frame, block_size=8):
    """
    Apply 2D block DCT and inverse DCT.
    :param frame: input image (grayscale)
    :param block_size: block size (default 8x8)
    :return: reconstructed image
    """
    if frame is None:
        raise ValueError("Input frame is None")
    
    gray = frame
    if len(frame.shape) == 3:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    h, w = gray.shape
    reconstructed = np.zeros_like(gray, dtype=np.float32)
    
    for i in range(0, h, block_size):
        for j in range(0, w, block_size):
            block = gray[i:i+block_size, j:j+block_size].astype(np.float32)
            dct_block = cv2.dct(block)
            # optional coefficient thresholding
            dct_block[np.abs(dct_block)<1] = 0
            idct_block = cv2.idct(dct_block)
            reconstructed[i:i+block_size, j:j+block_size] = idct_block
    
    reconstructed = np.clip(reconstructed,0,255).astype(np.uint8)
    return reconstructed

def process_image():
    img = cv2.imread('image.jpg')
    if img is None:
        print('Error: Image not found.')
        return
    
    out = block_dct(img, block_size=8)
    cv2.imwrite('output_dct.jpg', out)

if __name__ == '__main__':
    process_image()