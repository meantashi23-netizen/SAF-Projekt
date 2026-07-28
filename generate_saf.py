import numpy as np
from scipy.io import wavfile

# --- PARAMETER AUS DEM BILD/SAF-DIAGRAMM ---
sample_rate = 44100  # 44.1 kHz Standard-Audio
duration = 8.0       # Dauer in Sekunden
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# 1. Grundfrequenz & Tripleslit (3 gegeneinander verschobene Phasen/Quellen)
base_freq = 110.0  # A2
phase_shift = 2 * np.pi / 3  # 120° Phasensprung für Tripleslit-Symmetrie

# Drei Interferenz-Wellen (Tripleslit Network)
wave1 = np.sin(2 * np.pi * base_freq * t)
wave2 = np.sin(2 * np.pi * base_freq * t + phase_shift)
wave3 = np.sin(2 * np.pi * base_freq * t + 2 * phase_shift)
tripleslit = (wave1 + wave2 + wave3) / 3.0

# 2. Rekursives Fraktalband (N = 16 effektive Obertöne / Kohärenz-Peaks)
# Rekursive Staffelung analog zu \lambda / N = 16
fractal_band = np.zeros_like(t)
N_effekt = 16

for n in range(1, N_effekt + 1):
    # Obertöne mit fraktalem Amplitudenabfall (1/n) & Phasenversatz
    harmonic_freq = base_freq * (1 + (n / 16.0))
    fractal_band += (1.0 / n) * np.sin(2 * np.pi * harmonic_freq * t * (1 + 0.05 * np.sin(t)))

# 3. 5-Dimensionalitäts-Faltung (Omakoma Phase Modulation / Torus-Rotation)
# Faltung der Signale über komplexe Modulationsfrequenzen (5D-Knoten Kohärenz \rho = 99.8%)
f_5d_1 = 0.5   # Langsame Torus-Rotation
f_5d_2 = 3.33  # Omakoma Interferenz-Modulation
f_5d_3 = 13.0  # Kohärenz-Peak Modulationsfrequenz

mod_5d = np.cos(2 * np.pi * f_5d_1 * t) * np.sin(2 * np.pi * f_5d_2 * t + np.sin(2 * np.pi * f_5d_3 * t))

# Synthese & Modulation (SAF Omakoma Blend)
coherence_node = 0.998  # 99.8% Kohärenz-Gewichtung
audio_signal = (tripleslit * 0.4 + fractal_band * 0.4) * (1 + 0.3 * mod_5d) * coherence_node

# Normalisierung auf Int16 Audiobereich
audio_signal = audio_signal / np.max(np.abs(audio_signal))
audio_int16 = (audio_signal * 32767).astype(np.int16)

# Speichern als .WAV
output_filename = "SAF_Omakoma_5D_Tripleslit.wav"
wavfile.write(output_filename, sample_rate, audio_int16)

print(f"[SAF ANALYTICS] Waveform erfolgreich generiert: {output_filename}")
