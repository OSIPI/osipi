import numpy as np
from scipy import ndimage


def median_filter(signal):
    """
    Apply a median filter to a signal.
    """
    return ndimage.median_filter(signal, size=(3, 3, 1, 1))


def add_gaussian_noise(signal, mean=0, std=1):
    """
    Add Gaussian noise to the 4 MR data.
    """
    return signal + np.random.normal(mean, std, signal.shape)


def add_rician_noise(signal, mean=0, std=1):
    """
    Add Rician noise to the 4D MR data.
    """
    noise_real = np.random.normal(0, std, signal.shape)
    noise_imag = np.random.normal(0, std, signal.shape)
    noisy_signal = np.sqrt(signal**2 + noise_real**2 + noise_imag**2)
    return noisy_signal
