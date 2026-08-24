import numpy as np, scipy.io.wavfile as w, scipy.signal as s

SR, DUR = 44100, 10
t = np.linspace(0, DUR, SR * DUR, endpoint=False)

# Metrik: 3/4-Takt @ 96 BPM / 192 BPM
BPM = 96.00
TRIPLET_FREQ = (BPM / 60.0) * 3 * 3

# Mathematische Konstanten
PHI = (1.0 + np.sqrt(5.0)) / 2.0  # Goldener Schnitt
FEIGENBAUM_DELTA = 4.669201609102990

def gen_saf_n1080_fibonacci(v, freq_base, phi_dispersion, chaos_r):
    N = 1080
    k_vec = np.arange(1, N + 1)[:, None] # Shape (1080, 1)

    # 1. Goldener Schnitt Modulation & Phase Grid (N=1080)
    # Frequenz-Verteilung basiert auf der Fibonacci-Spirale / PHI-Skalierung
    freq_k = freq_base * (1.0 + (phi_dispersion * 0.00004) * (k_vec ** (1.0 / PHI)))
    
    # Phasen-Verschiebung im 6D-Raum mit PHI-Multiplikator
    phase_k = (k_vec * np.pi / (4.0 * PHI)) + np.sin(2 * np.pi * (TRIPLET_FREQ / 2.0) * t) * 0.02
    
    # Superposition aller 1080 Oszillatoren mit PHI-Dämpfung
    node_waves = np.sin(2 * np.pi * freq_k * t + phase_k) / (k_vec ** 0.15)
    matrix_1080 = np.sum(node_waves, axis=0) / np.sqrt(N)

    # 2. Bifurkation & Edge-of-Chaos Injection
    x = 0.5 * np.ones(len(t))
    for i in range(1, len(t)):
        x[i] = chaos_r * x[i-1] * (1.0 - x[i-1])
    chaos_mod = np.interp(t, np.linspace(0, DUR, len(x)), x) - 0.5

    # Combine Core Signal
    raw_core = matrix_1080 + 0.12 * chaos_mod

    # 3. Spatial Multi-Tap Dispersion (Hypercube Phi-Grid)
    del_l = int(SR * 0.005 * phi_dispersion * PHI)
    del_r = int(SR * 0.013 * phi_dispersion * PHI)

    pan_mod = np.cos(2 * np.pi * (TRIPLET_FREQ / 3.0) * t * PHI)
    
    mix_l = raw_core * (1.0 + 0.3 * pan_mod) + np.roll(raw_core, del_l) * 0.2
    mix_r = raw_core * (1.0 - 0.3 * pan_mod) + np.roll(raw_core, del_r) * 0.2

    # High-End Bandpass / Dynamic Air Filtering
    sos = s.butter(4, [max(16, freq_base * 0.4), min(20000, freq_base * 10.0)], btype='bandpass', output='sos', fs=SR)
    mix_l = s.sosfilt(sos, mix_l)
    mix_r = s.sosfilt(sos, mix_r)

    # Normalisierung
    mix_l = np.nan_to_num(mix_l)
    mix_r = np.nan_to_num(mix_r)
    m = np.max(np.abs([mix_l, mix_r]))
    if m == 0: m = 1.0

    audio_out = (np.vstack((mix_l/m, mix_r/m)).T * 32767).astype(np.int16)
    w.write(f"opt_saf_{v}.wav", SR, audio_out)

# 8 Neue N=1080 Fibonacci-Samples (v140 - v147)
config = [
    ('v140_n1080_sub_c0',       16.35,  1.0, 3.85), # Ground Zero N=1080 C0
    ('v141_n1080_bass_c1',      32.70,  1.3, 3.89), # Deep Phi Bass C1
    ('v142_phi_root_c2',        65.41,  1.6, 3.93), # Resonant Root C2
    ('v143_phi_fifth_g2',       98.00,  2.0, 3.96), # Golden Quinte G2
    ('v144_n1080_mid_c3',      130.81,  2.4, 3.98), # High-Density Phi Mid C3
    ('v145_n1080_terz_e3',     164.81,  2.8, 3.99), # Spatial Terz E3
    ('v146_phi_high_c4',       261.63,  3.2, 3.996),# Apex High Beam C4
    ('v147_phi_top_c5',        523.25,  3.8, 3.999) # Absolute N=1080 Singularity C5
]

for v, f_hz, disp, r_val in config:
    gen_saf_n1080_fibonacci(v, f_hz, disp, r_val)
    print(f"[N=1080 Phi Engine] opt_saf_{v}.wav ({f_hz} Hz @ 96/192 BPM) generiert.")
