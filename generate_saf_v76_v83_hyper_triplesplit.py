import numpy as np, scipy.io.wavfile as w, scipy.signal as s

SR, DUR = 44100, 10
t = np.linspace(0, DUR, SR * DUR, endpoint=False)

# Metrik: 3/4-Takt @ 96 BPM mit Polyrhythmischem Triolen-Gitter
BPM = 96.00
TRIPLET_FREQ = (BPM / 60.0) * 3 * 3  # 14.4 Hz Base
POLY_FREQ = TRIPLET_FREQ * (4.0 / 3.0)  # 19.2 Hz Polyrhythmic Overlay

def gen_hyper_triplesplit_saf(v, freq_base, resonance_q, poly_blend, chaos_r):
    # 1. Triolen- & Polyrhythmische Hüllkurven-Fusion
    triplet_env = 0.5 * (1.0 + np.sin(2 * np.pi * TRIPLET_FREQ * t))
    poly_env = 0.5 * (1.0 + np.cos(2 * np.pi * POLY_FREQ * t))
    combined_env = (1.0 - poly_blend) * triplet_env + poly_blend * poly_env

    # 2. Advanced Multi-Shell Triplesplit (Phasenverschiebung mit xπ)
    phi1 = 2 * np.pi * freq_base * t
    phi2 = 2 * np.pi * (freq_base * 1.50) * t + (np.pi / 3.0) * resonance_q
    phi3 = 2 * np.pi * (freq_base * 2.02) * t + (2 * np.pi / 3.0) * resonance_q

    core_signal = (np.sin(phi1) + 0.8 * np.sin(phi2) + 0.6 * np.sin(phi3)) / 2.4

    # 3. Chaos Akkumulator (High r-Value)
    x = 0.5 * np.ones(len(t))
    for i in range(1, len(t)):
        x[i] = chaos_r * x[i-1] * (1.0 - x[i-1])
    chaos_mod = np.interp(t, np.linspace(0, DUR, len(x)), x) - 0.5

    # 4. Synthese & Dynamischer Resonanzfilter
    raw_mix = (core_signal + 0.25 * chaos_mod) * combined_env
    
    # Resonanz-Filterung (Bandpass)
    sos = s.butter(4, [max(20, freq_base * 0.8), min(20000, freq_base * 3.5)], btype='bandpass', output='sos', fs=SR)
    filtered = s.sosfilt(sos, raw_mix)

    # 5. Dynamic Pan Trajectory (Triplesplit Spatial Rotation)
    mix_l = filtered * np.cos(2 * np.pi * (TRIPLET_FREQ / 6.0) * t)
    mix_r = filtered * np.sin(2 * np.pi * (TRIPLET_FREQ / 6.0) * t)

    # Output Normalisierung
    mix_l = np.nan_to_num(mix_l)
    mix_r = np.nan_to_num(mix_r)
    m = np.max(np.abs([mix_l, mix_r]))
    if m == 0: m = 1.0

    audio_out = (np.vstack((mix_l/m, mix_r/m)).T * 32767).astype(np.int16)
    w.write(f"opt_saf_{v}.wav", SR, audio_out)

# 8 Finale Samples (v76 - v83)
config = [
    ('v76_hyper_sub_c1',        32.70,  1.1, 0.2, 3.65), # Deep Poly Sub (C1)
    ('v77_hyper_root_c2',       65.41,  1.3, 0.3, 3.73), # Low Punch (C2)
    ('v78_poly_fifth_g2',       98.00,  1.5, 0.4, 3.81), # Low Mid Quinte (G2)
    ('v79_poly_octave_c3',     130.81,  1.7, 0.5, 3.88), # Mid Octave (C3)
    ('v80_triplesplit_e3',     164.81,  1.9, 0.5, 3.92), # Mid Terz (E3)
    ('v81_triplesplit_g3',     196.00,  2.1, 0.4, 3.95), # High Quinte (G3)
    ('v82_hyper_sharp_c4',     261.63,  2.4, 0.3, 3.98), # Peak High (C4)
    ('v83_hyper_fusion_e4',    329.63,  2.8, 0.2, 3.99)  # Ultra Fusion Top (E4)
]

for v, f_hz, res_q, poly_b, r_val in config:
    gen_hyper_triplesplit_saf(v, f_hz, res_q, poly_b, r_val)
    print(f"[Hyper Triplesplit] opt_saf_{v}.wav ({f_hz} Hz @ 96 BPM) generiert.")
