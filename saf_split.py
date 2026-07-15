import numpy as np
import matplotlib.pyplot as plt

def generate_saf_bifurcation(width=1920, height=1080, t_correction=1.00239):
    print("[SaF 29.3.3] Starte Dual-Split Bifurkations-Mapping...")
    r_values = np.linspace(2.5, 4.0, width)
    iterations = 1000
    last = 300 
    
    x = 0.5 * np.ones(width) + (0.01 * np.cos(t_correction))
    
    r_out = []
    x_out = []

    for i in range(iterations):
        x = r_values * x * (1.0 - x)
        if i >= (iterations - last):
            r_out.append(r_values)
            x_out.append(x)
            
    return np.array(r_out), np.array(x_out)

r_data, x_data = generate_saf_bifurcation()

# Rendering & Styling für den Upload-Speicher
plt.figure(figsize=(16, 9), facecolor='#000000')
ax = plt.axes()
ax.set_facecolor('#000000')

# Smaragd-Alpha & Kosmisches Cyan Fusion
ax.plot(r_data, x_data, ', ', color='#00ffcc', alpha=0.3)

plt.axis('off')
plt.tight_layout()

# Speichern im aktuellen Verzeichnis
output_path = "saf_post_dual_split.png"
plt.savefig(output_path, dpi=300, facecolor='#000000')
print(f"[SaF Erfolg] Bild wurde erfolgreich generiert und abgelegt unter: {output_path}")
