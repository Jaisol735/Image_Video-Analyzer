import os
import cv2

def load_image(path: str, flags=cv2.IMREAD_COLOR):
    """Load image robustly with support for Windows paths.

    Returns the image array or None if not found.
    """
    # Accept both backslashes and forward slashes
    normalized = os.path.normpath(path)
    img = cv2.imread(normalized, flags)
    return img

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def save_image(output_dir: str, filename: str, image) -> str:
    ensure_dir(output_dir)
    normalized_dir = os.path.normpath(output_dir)
    out_path = os.path.join(normalized_dir, filename)
    cv2.imwrite(out_path, image)
    return out_path


