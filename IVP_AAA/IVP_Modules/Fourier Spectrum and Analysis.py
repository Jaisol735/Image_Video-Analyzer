import cv2
import numpy as np

def fourier_analysis(frame):
    """
    Compute 2D DFT, magnitude and phase spectra, and inverse transform.
    :param frame: input image (grayscale)
    :return: magnitude spectrum, phase spectrum, reconstructed image
    """
    if frame is None:
        raise ValueError("Input frame is None")
    
    gray = frame
    if len(frame.shape) == 3:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    f = np.fft.fft2(gray)
    fshift = np.fft.fftshift(f)
    
    magnitude_spectrum = 20*np.log1p(np.abs(fshift))
    phase_spectrum = np.angle(fshift)
    
    # inverse transform
    f_ishift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back).astype(np.uint8)
    
    return magnitude_spectrum, phase_spectrum, img_back

def process_image():
    img = cv2.imread('image.jpg')
    if img is None:
        print('Error: Image not found.')
        return
    
    mag, phase, recon = fourier_analysis(img)
    mag_norm = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    phase_norm = cv2.normalize(phase, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    cv2.imwrite('output_fourier_magnitude.jpg', mag_norm)
    cv2.imwrite('output_fourier_phase.jpg', phase_norm)
    cv2.imwrite('output_fourier_recon.jpg', recon)

if __name__ == '__main__':
    process_image()
