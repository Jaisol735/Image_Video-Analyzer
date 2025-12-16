"""
Log transformation for brightness compression.
Non-interactive, no GUI. Reads 'image.jpg' and writes 'output_log.jpg'.
"""
import cv2, numpy as np, os

def log_transform(img: np.ndarray, c: float = 1.0) -> np.ndarray:
    img_f = img.astype(np.float32)
    log_img = c * np.log1p(img_f)
    # explicit destination array to satisfy Pylance
    dst = np.zeros_like(log_img, dtype=np.float32)
    cv2.normalize(log_img, dst, 0, 255, cv2.NORM_MINMAX)
    return dst.astype(np.uint8)

def process_image():
    img = cv2.imread('image.jpg', cv2.IMREAD_UNCHANGED)
    if img is None:
        print("Error: cannot read image 'image.jpg'")
        return
    c = 1.0
    out = log_transform(img, c)
    cv2.imwrite('output_log.jpg', out.astype(np.uint8))

def process_video(path: str, c: float):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        print(f"Error: cannot open video '{path}'")
        return

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if w == 0 or h == 0:
        print("Error: invalid video dimensions")
        cap.release()
        return

    fourcc = getattr(cv2, 'VideoWriter_fourcc')(*'XVID')
    outv = cv2.VideoWriter('output_log.avi', fourcc, 20.0, (w, h))
    if not outv.isOpened():
        print("Warning: failed to open VideoWriter, skipping write")

    while True:
        ret, frame = cap.read()
        if not ret: break

        logf = log_transform(frame, c)
        if outv.isOpened():
            outv.write(logf.astype(np.uint8))

    cap.release()
    outv.release()

if __name__=="__main__":
    process_image()
