"""
Gaussian blur + sharpening (non-interactive).
Reads 'image.jpg' and writes 'output_sharp.jpg' and 'output_lap.jpg'.
"""
import cv2, numpy as np

def sharpen(img, ksize=5, sigma=1.0, strength=1.5):
    blur=cv2.GaussianBlur(img,(ksize,ksize),sigma)
    sharp=cv2.addWeighted(img,1+strength,blur,-strength,0)
    return sharp,blur

def laplacian_sharp(img):
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    lap=cv2.Laplacian(gray,cv2.CV_64F)
    sharp=np.uint8(np.clip(gray-lap,0,255))
    return sharp

if __name__=="__main__":
    path='image.jpg'
    img=cv2.imread(path)
    if img is None:
        print(f"Error: cannot read image '{path}'"); raise SystemExit
    k=5; s=1.0; st=1.5
    if k < 3: k = 3
    if k % 2 == 0: k += 1
    sharp,blur=sharpen(img,k,s,st)
    lap=laplacian_sharp(img)
    cv2.imwrite('output_sharp.jpg',sharp)
    cv2.imwrite('output_lap.jpg',lap)
