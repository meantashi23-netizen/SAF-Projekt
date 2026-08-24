import numpy as np
from scipy.io import wavfile

# --- COMMON GRID PARAMETERS ---
bpm = 960.0 / 11.0  # 87.272727... BPM
sample_rate = 44100
duration = 22.0     # Exakt 32 Beats / 22.0s
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
beat_dur = 60.0 / bpm
sixteenth_dur = beat_dur / 4.0

# Envelope Generator für Grid-Sync
def get_grid_envelope(pattern_type="standard"):
    env = np.zeros_like(t)
    for i in range(128):  # 128 Sechzehntel (32 Beats)
        t_start = i * sixteenth_dur
        idx = int(t_start * sample_rate)
        
        if pattern_type == "syncopated":
            # Offbeat Emphasis (Gebrauch für Variation 2)
            amp = 1.0 if i % 4 == 2 else (0.7 if i % 4 == 0 else 0.3)
            decay = 0.08 if i % 2 == 0 else 0.04
        elif pattern_type == "polyrhythmic":
            # 3/4 Überlagerung auf 4/4 Grid (Gebrauch für Variation 3)
            amp = 1.0 if i % 3 == 0 else 0.2
            decay = 0.09
        elif pattern_type == "half_speed":
            # Half-Time Pumping (Gebrauch für Variation 4)
            amp = 1.0 if i % 8 == 0 else (0.4 if i % 4 == 0 else 0.1)
            decay = 0.18
        else: # Standard Driving
            amp = 1.0 if i % 4 == 0 else (0.5 if i % 2 == 0 else 0.25)
            decay = 0.10
            
        t_e = t[idx:] - t_start
        e = amp * np.exp(-t_e / decay)
        len_add = min(len(e), len(t) - idx)
        env[idx:idx + len_add] += e[:len_add]
    return np.tanh(env)

# ==============================================================================
# VARIATION 1: Torus Geometry Rescale (Tiefe Sub-Bässe & Inversion)
# ==============================================================================
base_1 = 55.0  # Sub-Oktave (A1)
w1 = np.sin(2 * np.pi * base_1 * t)
w2 = np.sin(2 * np.pi * base_1 * t + (2*np.pi/3))
w3 = np.sin(2 * np.pi * base_1 * t + (4*np.pi/3))
tripleslit_1 = (w1 + w2 + w3) / 3.0

fractal_1 = sum((1.0 / n) * np.sin(2 * np.pi * base_1 * (1 + n/16.0) * t) for n in range(1, 17))
mod_1 = np.cos(2 * np.pi * (bpm/60.0/8.0) * t)
sig_1 = (tripleslit_1 * 0.6 + fractal_1 * 0.3) * (0.4 + 0.6 * get_grid_envelope("standard"))
sig_1 = sig_1 / np.max(np.abs(sig_1))
wavfile.write("SAF_Var1_Torus_Sub.wav", sample_rate, (sig_1 * 32767).astype(np.int16))

# ==============================================================================
# VARIATION 2: High-Frequency Interference Band (Fraktales Flimmern & Synkopen)
# ==============================================================================
base_2 = 220.0  # A3
fractal_2 = sum((1.0 / np.sqrt(n)) * np.sin(2 * np.pi * base_2 * (n / 2.0) * t) for n in range(1, 17))
mod_2 = np.sin(2 * np.pi * (bpm/60.0 * 4.0) * t)  # Schneller 1/16-Puls
sig_2 = fractal_2 * (0.2 + 0.8 * get_grid_envelope("syncopated")) * (1 + 0.2 * mod_2)
sig_2 = sig_2 / np.max(np.abs(sig_2))
wavfile.write("SAF_Var2_Fractal_Band.wav", sample_rate, (sig_2 * 32767).astype(np.int16))

# ==============================================================================
# VARIATION 3: Polyrhythmic 5D Network (3-gegen-4 Interferenz)
# ==============================================================================
base_3 = 110.0
w_poly1 = np.sin(2 * np.pi * base_3 * t)
w_poly2 = np.sin(2 * np.pi * base_3 * 1.5 * t) # Quinte
sig_3 = (w_poly1 + w_poly2) * get_grid_envelope("polyrhythmic")
sig_3 = sig_3 / np.max(np.abs(sig_3))
wavfile.write("SAF_Var3_Polyrhythmic_5D.wav", sample_rate, (sig_3 * 32767).astype(np.int16))

# ==============================================================================
# VARIATION 4: Half-Time Omakoma Core (Epischer Slow-Down & Sweep)
# ==============================================================================
sweep = np.linspace(55.0, 110.0, len(t))
sig_4 = np.sin(2 * np.pi * sweep * t) * get_grid_envelope("half_speed")
for n in [2, 4, 8, 16]:
    sig_4 += (1.0 / n) * np.sin(2 * np.pi * sweep * n * t)
sig_4 = sig_4 / np.max(np.abs(sig_4))
wavfile.write("SAF_Var4_HalfTime_Sweep.wav", sample_rate, (sig_4 * 32767).astype(np.int16))

print("[SAF SYSTEM] Alle 4 Variationen auf 87.2727 BPM / 22.0s gerendert!")
