import numpy as np
from scipy.io import wavfile

# --- EXACT GRID CALCULATIONS ---
bpm = 960.0 / 11.0  # 87.272727... BPM
sample_rate = 44100
duration = 22.0     # 32 Beats = exakt 22.0 Sekunden (16 Beats = 11.0s)
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

beat_duration = 60.0 / bpm  # 0.6875 Sek. pro Beat

# --- 1. BASE SAF / OMAKOMA SYNTHESIS ---
base_freq = 110.0  # A2
phase_shift = 2 * np.pi / 3

# Tripleslit Interferenz
wave1 = np.sin(2 * np.pi * base_freq * t)
wave2 = np.sin(2 * np.pi * base_freq * t + phase_shift)
wave3 = np.sin(2 * np.pi * base_freq * t + 2 * phase_shift)
tripleslit = (wave1 + wave2 + wave3) / 3.0

# N = 16 Fraktalband (\lambda / N = 16)
fractal_band = np.zeros_like(t)
for n in range(1, 17):
    harmonic_freq = base_freq * (1 + (n / 16.0))
    fractal_band += (1.0 / n) * np.sin(2 * np.pi * harmonic_freq * t)

# 5D Folded Geometry Modulation (Omakoma Node p=99.8%)
f_5d_1 = (bpm / 60.0) / 4.0
f_5d_2 = (bpm / 60.0) * 2.0
mod_5d = np.cos(2 * np.pi * f_5d_1 * t) * np.sin(2 * np.pi * f_5d_2 * t)

carrier = (tripleslit * 0.4 + fractal_band * 0.4) * (1 + 0.35 * mod_5d) * 0.998

# --- 2. RHYTHMIC GRID ENVELOPE (16th Note Grid) ---
beat_envelope = np.zeros_like(t)
sixteenth_duration = beat_duration / 4.0

for i in range(128):  # 32 Beats * 4 = 128 Sechzehntel
    t_start = i * sixteenth_duration
    idx_start = int(t_start * sample_rate)
    
    amp = 1.0 if i % 4 == 0 else (0.5 if i % 2 == 0 else 0.25)
    decay = 0.12 if i % 4 == 0 else 0.05
    
    t_env = t[idx_start:] - t_start
    env = amp * np.exp(-t_env / decay)
    
    len_to_add = min(len(env), len(t) - idx_start)
    beat_envelope[idx_start:idx_start + len_to_add] += env[:len_to_add]

# On-Grid Pump Modulation
rhythmic_signal = carrier * (0.3 + 0.7 * np.tanh(beat_envelope))

# Normalisierung & Export
rhythmic_signal /= np.max(np.abs(rhythmic_signal))
audio_int16 = (rhythmic_signal * 32767).astype(np.int16)

wavfile.write("SAF_Omakoma_5D_87.2727BPM.wav", sample_rate, audio_int16)
print("[SAF ANALYTICS] Waveform @ 87.2727 BPM (32 Beats / 22.0s) gerendert.")
