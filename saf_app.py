import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

print("--> SAF V29.3.5 Mandelbrot-Spectrum wird initialisiert...")

# 1. Gitter initialisieren
resolution = 300
x = np.linspace(-2.1, 0.6, resolution)
y = np.linspace(-1.25, 1.25, resolution)
X, Y = np.meshgrid(x, y)
C = X + 1j * Y

max_iter = 128
z = np.zeros_like(C)

# Speicher für Iterationsfolgen zur SAF-Analyse
signal_stack = np.zeros((max_iter, resolution, resolution), dtype=np.float32)

for i in range(max_iter):
    mask = np.abs(z) <= 2
    z[mask] = z[mask]**2 + C[mask]
    signal_stack[i] = np.abs(z)

# 2. Spektrale Analyse (SAF / FFT über die Zeitachse)
fft_spectrum = np.abs(np.fft.rfft(signal_stack, axis=0))

# Frequenzbänder aufteilen (WIF, MIF, HIF)
freq_low = np.mean(fft_spectrum[1:4, :, :], axis=0)    # Tiefe Frequenzen (WIF)
freq_mid = np.mean(fft_spectrum[5:16, :, :], axis=0)   # Mittlere Frequenzen (MIF)
freq_high = np.mean(fft_spectrum[17:, :, :], axis=0)   # Hohe Frequenzen (HIF)

# 3. Spektrale Farbauflösung (RGB Normalisierung)
def norm(arr):
    return (arr - np.min(arr)) / (np.ptp(arr) + 1e-8)

R = norm(np.log1p(freq_low))
G = norm(np.log1p(freq_mid))
B = norm(np.log1p(freq_high))

RGB = np.stack([R, G, B], axis=-1)

# 4. 3D-Abbildung (Höhenprofil basierend auf Gesamtfrequenzenergie)
Z_height = norm(np.log1p(np.sum(fft_spectrum[1:], axis=0)))

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot der 3D-Oberfläche
surf = ax.plot_surface(X, Y, Z_height, facecolors=RGB, rstride=1, cstride=1, linewidth=0, antialiased=False)

ax.set_title("SAF-Spektralanalyse der Mandelbrot-Menge (3D)", fontsize=14)
ax.set_xlabel("Re (c)")
ax.set_ylabel("Im (c)")
ax.set_zlabel("Spektrale Energie (Höhe)")
ax.view_init(elev=45, azim=-120)

print("--> Rendering abgeschlossen. Speichere 3D-Ansicht als Bild...")
plt.savefig("saf_3d_mandelbrot.png", dpi=300, bbox_inches='tight')

try:
    plt.show()
except Exception as e:
    print("Graphisches Display nicht verfügbar, Bild wurde als 'saf_3d_mandelbrot.png' gespeichert.")
