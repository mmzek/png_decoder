import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def fourier_transform(img):

    #converting grayscale img pixels into 2D floats array
    data = np.array(img, dtype=np.float64)

    #2D fast fourier transform
    fft = np.fft.fft2(data)

    #shifting zero-frequency component to the center
    fft_shift = np.fft.fftshift(fft)

    #scaling to log bc of big range
    magnitude = np.log1p(np.abs(fft_shift))

    #displaying FFT spectrum
    plt.figure("FFT Spectrum", figsize=(10, 5))
    plt.subplot(121)
    plt.imshow(img, cmap='gray')
    plt.title("Original (grayscale)")
    plt.axis('off')

    plt.subplot(122)
    plt.imshow(magnitude, cmap='gray')
    plt.colorbar(label='Log magnitude')
    plt.title("FFT Magnitude Spectrum")
    plt.axis('off')

    plt.savefig('fft_output.png', dpi=150, bbox_inches='tight')
    plt.show()
    return fft_shift, magnitude