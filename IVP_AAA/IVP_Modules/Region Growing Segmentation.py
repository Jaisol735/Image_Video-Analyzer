import cv2
import numpy as np

def region_growing(frame, seed_points, threshold=10):
    """
    Seed-based region growing on grayscale image.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if len(frame.shape)==3 else frame
    h, w = gray.shape
    mask = np.zeros((h,w), np.uint8)
    visited = np.zeros((h,w), np.bool_)

    def grow(x,y,seed_val):
        stack = [(x,y)]
        while stack:
            i,j = stack.pop()
            if visited[i,j]:
                continue
            visited[i,j] = True
            mask[i,j] = 255
            for di in [-1,0,1]:
                for dj in [-1,0,1]:
                    ni, nj = i+di, j+dj
                    if 0<=ni<h and 0<=nj<w and not visited[ni,nj]:
                        if abs(int(gray[ni,nj])-int(seed_val)) <= threshold:
                            stack.append((ni,nj))
    for sp in seed_points:
        grow(sp[0], sp[1], gray[sp[0], sp[1]])

    return mask

def process_image():
    img = cv2.imread('image.jpg')
    if img is None:
        print('Error: Image not found.')
        return
    
    h, w = img.shape[:2]
    seeds = [(h//2, w//2)]
    out = region_growing(img, seeds, threshold=10)
    cv2.imwrite('output_region_growing.jpg', out)

if __name__ == '__main__':
    process_image()
