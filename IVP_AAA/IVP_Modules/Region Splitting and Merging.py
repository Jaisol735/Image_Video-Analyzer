import cv2
import numpy as np

def region_split_merge(frame, max_depth=4, var_thresh=500):
    """
    Quadtree-like region splitting and merging based on variance.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if len(frame.shape)==3 else frame
    h, w = gray.shape
    result = np.zeros_like(gray)

    def split(x,y,width,height,depth):
        region = gray[y:y+height, x:x+width]
        if depth>=max_depth or np.var(region)<=var_thresh:
            result[y:y+height, x:x+width] = np.mean(region)
        else:
            hw, hh = width//2, height//2
            split(x, y, hw, hh, depth+1)
            split(x+hw, y, width-hw, hh, depth+1)
            split(x, y+hh, hw, height-hh, depth+1)
            split(x+hw, y+hh, width-hw, height-hh, depth+1)
    split(0,0,w,h,0)
    
    return result

def process_image():
    img = cv2.imread('image.jpg')
    if img is None:
        print('Error: Image not found.')
        return
    
    out = region_split_merge(img, max_depth=4, var_thresh=500)
    cv2.imwrite('output_split_merge.jpg', out)

if __name__ == '__main__':
    process_image()
