"""
Power-law (Gamma) transformation, non-interactive.
Reads 'image.jpg' and writes 'output_gamma.jpg'.
"""
import cv2, numpy as np

def gamma_correct(img, gamma=1.0):
    # protect against invalid gamma
    if gamma <= 0:
        return img.copy()
    inv = 1.0 / gamma
    table = np.array([(i/255.0)**inv * 255 for i in np.arange(256)]).astype("uint8")
    return cv2.LUT(img, table)

def interactive_gamma(img):
    # Removed GUI trackbar for non-interactive mode
    pass

def process_video(path,gamma):
    if gamma == 0:
        print("Slider mode not supported for video. Provide a numeric gamma > 0.")
        return
    cap=cv2.VideoCapture(path)
    if not cap.isOpened():
        print(f"Error: cannot open video '{path}'"); return
    while True:
        ret,frame=cap.read()
        if not ret: break
        out=gamma_correct(frame,gamma)
        cv2.imshow('Gamma Video',out)
        if cv2.waitKey(1) & 0xFF == 27: break
    cap.release();cv2.destroyAllWindows()

def process_image():
    img = cv2.imread('image.jpg')
    if img is None:
        print("Error: cannot read image 'image.jpg'")
        return
    
    # Safety: downscale very large images to avoid timeouts
    h, w = img.shape[:2]
    max_side = max(h, w)
    if max_side > 3000:
        scale = 3000.0 / max_side
        img = cv2.resize(img, (int(w*scale), int(h*scale)), interpolation=cv2.INTER_AREA)
    
    gamma = 1.2  # Default gamma value
    out = gamma_correct(img, gamma)
    cv2.imwrite('output_gamma.jpg', out)

if __name__=="__main__":
    process_image()
