import numpy as np, scipy.io.wavfile as w, scipy.signal as s

SR, DUR = 44100, 10
t = np.linspace(0, DUR, SR * DUR, endpoint=False)

# Metrik: 3/4-Takt @ 96 BPM / 192 BPM
BPM = 96.00
TRIPLET_FREQ = (BPM / 60.0) * 3 * 3

FEIGENBAUM_DELTA = 4.669201609102990
FEIGENBAUM_ALPHA = 2.502907875095892

def gen_saf_n457_phase_matrix(v, freq_base, dispersion_factor, chaos_r):
    # 1. 6D Trajektorie (nodal coordinates)
    tau   = np.sin(2 * np.pi * (TRIPLET_FREQ / 2.0) * t)
    phi   = np.cos(2 * np.pi * (TRIPLET_FREQ / 3.0) * t)
    theta = np.sin(2 * np.pi * (TRIPLET_FREQ / 4.0) * t)
    
    # 2. High-Density N=457 Phase Integration
    N = 457
    # Vektorisierte Berechnung der 457 Knotenpunkte zur Performance-Optimierung
    k_vec = np.arange(1, N + 1)[:, None] # Shape (457, 1)
    
    # Phasen-Verschiebung basierend auf Pi/4 + Nodal-Modulation
    phase_k = (k_vec * np.pi / 4.0) + (tau * 0.05 * FEIGENBAUM_ALPHA)
    freq_k = freq_base * (1.0 + (dispersion_factor * 0.0001) * (k_vec - 1))
    
    # Superposition aller 457 Wellen
    node_waves = np.sin(2 * np.pi * freq_k * t + phase_k)
    matrix_sum = np.sum(node_waves, axis=0) / np.sqrt(N) # Quadratische Normalisierung

    # 3. Bifurkation & Tripleslit Interferenz
    x = 0.5 * np.ones(len(t))
    for i in range(1, len(t)):
        x[i] = chaos_r * x[i-1] * (1.0 - x[i-1])
    chaos_mod = np.interp(t, np.linspace(0, DUR, len(x)), x) - 0.5

    # Phasen-Interferenz (Tripleslit Core Modulation)
    phi1 = 2 * np.pi * freq_base * t
    phi2 = 2 * np.pi * (freq_base * 1.5) * t + (np.pi / 4.0)
    phi3 = 2 * np.pi * (freq_base * 2.0) * t + (np.pi / 2.0)
    tripleslit = (np.sin(phi1) + 0.7 * np.sin(phi2) + 0.5 * np.cos(phi3)) / 2.2

    # SAF Fusion
    fused = matrix_sum + 0.3 * tripleslit + 0.15 * chaos_mod

    # 4. 5D Spatial Stereo Dispersion
    del_l = int(SR * 0.008 * dispersion_factor)
    del_r = int(SR * 0.015 * dispersion_factor)

    mix_l = fused * (1.0 + 0.35 * phi) + np.roll(fused, del_l) * 0.25
    mix_r = fused * (1.0 - 0.35 * phi) + np.roll(fused, del_r) * 0.25

    # Bandpass-Filterung
    sos = s.butter(4, [max(16, freq_base * 0.4), min(20000, freq_base * 8.0)], btype='bandpass', output='sos', fs=SR)
    mix_l = s.sosfilt(sos, mix_l)
    mix_r = s.sosfilt(sos, mix_r)

    # Output Scaling
    mix_l = np.nan_to_num(mix_l)
    mix_r = np.nan_to_num(mix_r)
    m = np.max(np.abs([mix_l, mix_r]))
    if m == 0: m = 1.0

    audio_out = (np.vstack((mix_l/m, mix_r/m)).T * 32767).astype(np.int16)
    w.write(f"opt_saf_{v}.wav", SR, audio_out)

# 8 Neue N=457 Phase Samples (v132 - v139)
config = [
    ('v132_n457_sub_c0',        16.35,  1.0, 3.86), # Deep N=457 Sub C0
    ('v133_n457_bass_c1',       32.70,  1.2, 3.90), # Dense Bass C1
    ('v134_n457_root_c2',       65.41,  1.5, 3.94), # Phase Root C2
    ('v135_n457_fifth_g2',      98.00,  1.8, 3.96), # Phase Quinte G2
    ('v136_n457_mid_c3',       130.81,  2.2, 3.98), # High-Density Mid C3
    ('v137_n457_terz_e3',      164.81,  2.5, 3.99), # Dense Terz E3
    ('v138_n457_high_c4',      261.63,  3.0, 3.996),# Ultra Phase High C4
    ('v139_n457_apex_c5',      523.25,  3.5, 3.999) # N=457 Apex Top C5
]

for v, f_hz, disp, r_val in config:
    gen_saf_n457_phase_matrix(v, f_hz, disp, r_val)
    print(f"[SAF N=457 Engine] opt_saf_{v}.wav ({f_hz} Hz @ 96/192 BPM) generiert.")
