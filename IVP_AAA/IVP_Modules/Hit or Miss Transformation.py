import cv2
import numpy as np
from scipy.ndimage import binary_hit_or_miss
from typing import Optional, cast

def hit_or_miss(frame: np.ndarray, structure1: np.ndarray, structure2: Optional[np.ndarray] = None) -> np.ndarray:
    """
    Perform morphological hit-or-miss transformation on a binary image.

    :param frame: Input image (grayscale or color)
    :param structure1: Foreground structuring element
    :param structure2: Optional background structuring element
    :return: Hit-or-miss result as uint8 image (0 or 255)
    """
    if frame is None:
        raise ValueError("Input frame is None")

    # Convert color image to grayscale if needed
    if len(frame.shape) == 3:
        frame_gray: np.ndarray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:
        frame_gray: np.ndarray = frame

    # Convert grayscale image to binary
    binary: np.ndarray = frame_gray > 127

    # Perform hit-or-miss transformation
    result: Optional[np.ndarray] = binary_hit_or_miss(binary, structure1=structure1, structure2=structure2)
    assert result is not None, "binary_hit_or_miss returned None"
    # narrow the type for the type checker
    result = cast(np.ndarray, result)

    # Convert boolean array to uint8 image
    return result.astype(np.uint8) * 255


def process_image():
    frame: Optional[np.ndarray] = cv2.imread('image.jpg')
    if frame is None:
        print("Error: Image not found.")
        return
    
    structure1: np.ndarray = np.array([[0, 1, 0],
                                      [1, 1, 1],
                                      [0, 1, 0]], dtype=bool)
    structure2: np.ndarray = np.array([[1, 0, 1],
                                      [0, 0, 0],
                                      [1, 0, 1]], dtype=bool)
    result_img: np.ndarray = hit_or_miss(frame, structure1, structure2)
    cv2.imwrite("output_hit_or_miss.png", result_img)

if __name__ == "__main__":
    process_image()
