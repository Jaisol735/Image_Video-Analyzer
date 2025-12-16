import cv2
import numpy as np
from PIL import Image

def other_color_models(frame):
    """
    Convert to HSV, HSI, YUV, and CMYK (via PIL) and visualize channels.
    """
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)

    # CMYK conversion via PIL
    pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    cmyk = pil_img.convert('CMYK')

    return {'HSV':hsv, 'YUV':yuv, 'CMYK':cmyk}

def process_image():
    img = cv2.imread('image.jpg')
    if img is None:
        print('Error: Image not found.')
        return
    
    out = other_color_models(img)
    # Save the first channel images for quick reference
    cv2.imwrite('output_hsv_h.jpg', out['HSV'][:,:,0])
    cv2.imwrite('output_yuv_y.jpg', out['YUV'][:,:,0])
    cmyk = np.array(out['CMYK'])
    cv2.imwrite('output_cmyk_c.jpg', cmyk[:,:,0])

if __name__ == '__main__':
    process_image()
