# video_motion.py
import cv2
import numpy as np

def motion_estimation(video_path):
    """
    Compute block-based motion vectors using simple exhaustive search.
    """
    cap = cv2.VideoCapture(video_path)
    ret, prev = cap.read()
    prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
    block_size = 16
    motion_frames = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mv_frame = frame.copy()

        h, w = gray.shape
        for y in range(0, h-block_size, block_size):
            for x in range(0, w-block_size, block_size):
                block = gray[y:y+block_size, x:x+block_size]
                best_dx, best_dy, min_err = 0, 0, 1e10
                # Exhaustive search
                for dy in range(-4,5):
                    for dx in range(-4,5):
                        ny, nx = y+dy, x+dx
                        if 0<=ny<h-block_size and 0<=nx<w-block_size:
                            candidate = prev_gray[ny:ny+block_size, nx:nx+block_size]
                            err = np.sum((block - candidate)**2)
                            if err < min_err:
                                min_err = err; best_dx, best_dy = dx, dy
                cv2.arrowedLine(mv_frame, (x+block_size//2, y+block_size//2),
                                (x+block_size//2+best_dx*2, y+block_size//2+best_dy*2),
                                (0,0,255), 1)
        motion_frames.append(mv_frame)
        prev_gray = gray.copy()
    
    cap.release()
    return motion_frames

def process_image():
    path = 'image.jpg'
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        print('Error: cannot open video.')
        return
    
    cap.release()
    frames = motion_estimation(path)
    if frames:
        h, w = frames[0].shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        outv = cv2.VideoWriter('output_motion.avi', fourcc, 20.0, (w, h))
        if outv.isOpened():
            for f in frames:
                outv.write(f)
            outv.release()

if __name__ == '__main__':
    process_image()