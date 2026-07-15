plt.savefig("/data/data/com.termux/files/home/storage/downloads/fraktal_neu.png")
# Ändere die cmap im Code für den "Spektral-Look"
# cmap='magma' -> Für den goldenen Glanz
# cmap='twilight' -> Für den spektralen Übergang
# cmap='inferno' -> Für die Alpha-Fusion-Hitze

plt.imshow(img.T, cmap='magma', interpolation='bilinear')
import numpy as np
import matplotlib.pyplot as plt
import sys

# Wir nehmen das erste Argument, falls vorhanden, sonst 'magma' als Standard
farb_schema = sys.argv[1] if len(sys.argv) > 1 else 'magma'

def berechne_fraktal():
    print(f"Starte Berechnung mit Farbe: {farb_schema}")
    # ... (Dein restlicher Code hier) ...
    # Ersetze in plt.imshow(divtime, cmap='magma') durch:
    plt.imshow(divtime, cmap=farb_schema)
    plt.axis('off')
    plt.savefig("fraktal_neu.png")
    print(f"Fertig! Bild gespeichert als: fraktal_neu.png (Farbe: {farb_schema})")

if __name__ == "__main__":
    berechne_fraktal()
import numpy as np
import matplotlib.pyplot as plt

def berechne_fraktal():
    x, y = np.ogrid[-2:1:300j, -1.5:1.5:300j]
    c = x + y*1j
    z = c
    divtime = 30 + np.zeros(z.shape, dtype=int)
    for i in range(30):
        z = z**2 + c
        diverge = z*np.conj(z) > 2**2
        div_now = diverge & (divtime == 30)
        divtime[div_now] = i
        z[diverge] = 2
    plt.imshow(divtime, cmap='magma')
    plt.axis('off')
    plt.savefig("fraktal_neu.png")
    print("Fertig! Bild gespeichert: fraktal_neu.png")

if __name__ == "__main__":
    berechne_fraktal()
