import numpy as np, scipy.io.wavfile as w, scipy.signal as s

SR, DUR = 44100, 10
t = np.linspace(0, DUR, SR * DUR, endpoint=False)

# Metrik: 3/4-Takt @ 96 BPM / 192 BPM Modulationsraster
BPM = 96.00
TRIPLET_FREQ = (BPM / 60.0) * 3 * 3

def gen_saf_hyperspace_n16(v, freq_base, nodal_weight, chaos_r):
    # 1. 6D Nodal Coordinates Engine [tau, phi, theta, kappa, lambda, mu]
    tau   = np.sin(2 * np.pi * (TRIPLET_FREQ / 2.0) * t)
    phi   = np.cos(2 * np.pi * (TRIPLET_FREQ / 3.0) * t)
    theta = np.sin(2 * np.pi * (TRIPLET_FREQ / 4.0) * t)
    kappa = np.cos(2 * np.pi * (TRIPLET_FREQ / 6.0) * t)
    lam   = np.sin(2 * np.pi * (TRIPLET_FREQ / 8.0) * t)
    mu    = np.cos(2 * np.pi * (TRIPLET_FREQ / 12.0) * t)

    # 2. Sigma-Pi/4 Coherent Matrix (N=16 Nodes Integration)
    nodes = []
    for k in range(1, 17):
        # Phase-shift pro Knoten auf Pi/4 Basis
        phase_k = (k * np.pi / 4.0) + (tau * 0.1)
        node_wave = np.sin(2 * np.pi * (freq_base * (1.0 + 0.03 * (k - 1))) * t + phase_k)
        nodes.append(node_wave)
    
    matrix_sum = np.sum(nodes, axis=0) / 4.0

    # 3. Bifurkations-Feeder & Chaos
    x = 0.5 * np.ones(len(t))
    for i in range(1, len(t)):
        x[i] = chaos_r * x[i-1] * (1.0 - x[i-1])
    chaos_mod = np.interp(t, np.linspace(0, DUR, len(x)), x) - 0.5

    # 4. Multi-Dimensional Stereo Projection
    raw_core = matrix_sum + 0.2 * chaos_mod * nodal_weight

    # Spatial Multi-Tap Delay Line (Hyper-Tessellation)
    del_l1 = int(SR * 0.007 * nodal_weight)
    del_l2 = int(SR * 0.019 * nodal_weight)
    del_r1 = int(SR * 0.013 * nodal_weight)
    del_r2 = int(SR * 0.025 * nodal_weight)

    mix_l = raw_core * (1.0 + 0.3 * phi) + np.roll(raw_core, del_l1) * 0.35 - np.roll(raw_core, del_l2) * 0.15
    mix_r = raw_core * (1.0 - 0.3 * phi) + np.roll(raw_core, del_r1) * 0.35 + np.roll(raw_core, del_r2) * 0.15

    # Spektrale Filterung & Bandpass
    sos = s.butter(4, [max(16, freq_base * 0.5), min(20000, freq_base * 6.0)], btype='bandpass', output='sos', fs=SR)
    mix_l = s.sosfilt(sos, mix_l)
    mix_r = s.sosfilt(sos, mix_r)

    # Normalisierung
    mix_l = np.nan_to_num(mix_l)
    mix_r = np.nan_to_num(mix_r)
    m = np.max(np.abs([mix_l, mix_r]))
    if m == 0: m = 1.0

    audio_out = (np.vstack((mix_l/m, mix_r/m)).T * 32767).astype(np.int16)
    w.write(f"opt_saf_{v}.wav", SR, audio_out)

# 8 Neue Hyperspace Projection Samples (v124 - v131)
config = [
    ('v124_hyper_sub_c0',       16.35,  1.0, 3.84), # N=16 Sub C0
    ('v125_hyper_bass_c1',      32.70,  1.4, 3.89), # N=16 Bass C1
    ('v126_nodal_root_c2',      65.41,  1.8, 3.93), # Coherent Punch C2
    ('v127_nodal_fifth_g2',     98.00,  2.2, 3.96), # Coherent Quinte G2
    ('v128_matrix_mid_c3',     130.81,  2.6, 3.98), # Hyperspace Mid C3
    ('v129_matrix_terz_e3',    164.81,  3.0, 3.99), # Hyperspace Terz E3
    ('v130_coherent_high_c4',  261.63,  3.5, 3.995),# N16 High Beam C4
    ('v131_coherent_top_c5',   523.25,  4.0, 3.999) # Hyperspace Apex C5
]

for v, f_hz, n_w, r_val in config:
    gen_saf_hyperspace_n16(v, f_hz, n_w, r_val)
    print(f"[Hyperspace N=16 SAF] opt_saf_{v}.wav ({f_hz} Hz @ 96/192 BPM) generiert.")
