import os
import numpy as np
import scipy.io.wavfile as w
import scipy.signal as s

# System Parameter
SR = 44100
DUR = 10
BPM = 96.00
f_base = 261.63 # C4
r_chaos = 3.996
periodic_factor = 457.0 / 33.3333
saf_coefficient = 196.8334523

# Zeit-Vektor
t = np.linspace(0, DUR, SR * DUR, endpoint=False)

# 1/16 Quantisierungs-Puls
quant_1_16 = np.sin(2 * np.pi * (16.0 * BPM / 60.0) * t)

# Chaos-Modulation (Logistische Karte)
x = 0.5 * np.ones(len(t))
for i in range(1, len(t)):
    x[i] = r_chaos * x[i-1] * (1.0 - x[i-1])
chaos_mod = np.interp(t, np.linspace(0, DUR, len(x)), x) - 0.5

# Fraktaler Wellenbaum (16 Branches)
branches = [np.sin(2 * np.pi * (f_base * (1.0 + (b * 0.002 * periodic_factor))) * t + (b * np.pi / 4.0) + (quant_1_16 * 0.1)) for b in range(1, 17)]
tree_sum = np.sum(branches, axis=0) / 4.0 # Normalisierung

# SAF Void-Störsignal / Phasen-Kreuzung
phase_cross = np.sin(2 * np.pi * (saf_coefficient / 10.0) * t + (np.pi / 4.0))
void_stör = np.sin(2 * np.pi * f_base * 0.5 * t) * phase_cross * 0.25

# SAF Audio Fusion
fused_signal = tree_sum + (3.2 * 0.2 * chaos_mod) + void_stör

# Räumliche Fokussierung (Panning/Hass-Effekt)
pan_wave = np.sin(2 * np.pi * ((BPM / 60.0) * 2.25) * t)
mix_l = fused_signal * (1.0 + 0.35 * pan_wave) + np.roll(fused_signal, int(SR * 0.0192)) * 0.25
mix_r = fused_signal * (1.0 - 0.35 * pan_wave) + np.roll(fused_signal, int(SR * 0.0448)) * 0.25

# Finaler Bandpass & Normalisierung
sos = s.butter(4, [100, 20000], btype='bandpass', output='sos', fs=SR)
mix_l = s.sosfilt(sos, mix_l)
mix_r = s.sosfilt(sos, mix_r)
m = np.max(np.abs([mix_l, mix_r]))
audio_out = (np.vstack((mix_l/m, mix_r/m)).T * 32767).astype(np.int16)

# Export
filename = 'opt_saf_v154_c4_16_grundierung.wav'
w.write(filename, SR, audio_out)
print(f'SUCCESS: {filename} erzeugt!')
