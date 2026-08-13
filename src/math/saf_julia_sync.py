import numpy as np

def calculate_julia_c(spectral_bands):
    a = np.mean(spectral_bands[0:3]) * 0.78
    b = np.mean(spectral_bands[3:7]) * 0.156
    return complex(a, b)
