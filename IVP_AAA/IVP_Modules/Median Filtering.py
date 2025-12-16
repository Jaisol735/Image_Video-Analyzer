"""
MEDIAN FILTER – removes salt-and-pepper noise, supports image/video, variable kernel.
"""
import cv2, numpy as np, os

def median_filter(img,k):
    return cv2.medianBlur(img,k)

def process_image():
    img=cv2.imread('image.jpg')
    if img is None:
        print("Error: cannot read image 'image.jpg'")
        return
    k = 5
    if k < 3: k = 3
    if k % 2 == 0: k += 1
    out=median_filter(img,k)
    cv2.imwrite('output_median.jpg',out)

def process_video(path,k):
    cap=cv2.VideoCapture(path)
    if not cap.isOpened():
        print(f"Error: cannot open video '{path}'"); return
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if w == 0 or h == 0:
        print("Error: invalid video dimensions"); cap.release(); return
    # use getattr to avoid attribute-access diagnostics
    fourcc = getattr(cv2, 'VideoWriter_fourcc')(*'XVID')
    outv=cv2.VideoWriter('output_median.avi',fourcc,20.0,(w,h))
    if not outv.isOpened():
        print("Warning: VideoWriter failed; output won't be saved")
    while True:
        ret,frame=cap.read()
        if not ret:break
        f=median_filter(frame,k)
        if outv.isOpened():
            outv.write(f.astype(np.uint8))
    cap.release();outv.release()

if __name__=="__main__":
    process_image()
