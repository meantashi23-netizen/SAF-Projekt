import numpy as np, scipy.io.wavfile as w, scipy.signal as s

SR, DUR = 44100, 10
t = np.linspace(0, DUR, SR * DUR, endpoint=False)

# Metrik: 3/4-Takt @ 96 BPM mit Rubber-Backline Triolen
BPM = 96.00
TRIPLET_FREQ = (BPM / 60.0) * 3 * 3  # 14.4 Hz Trioles Grid

def gen_triplesplit_rubber_saf(v, freq_base, xpi_sharpness, rubber_resonance, chaos_r):
    # 1. 3/4 Triolen Envelope mit Rubber-Resonanz
    triplet_pulse = 0.5 * (1.0 + np.sin(2 * np.pi * TRIPLET_FREQ * t))
    rubber_backline = np.exp(-3.0 * ((t * TRIPLET_FREQ) % 1.0)) * rubber_resonance
    envelope = triplet_pulse * (0.6 + 0.4 * rubber_backline)

    # 2. Triplesplit Phase-Sharpness Modulation (xπ)
    phase_sharp = np.sin(2 * np.pi * freq_base * t + (np.pi / 4.0) * xpi_sharpness * np.sin(2 * np.pi * TRIPLET_FREQ * t))
    
    # 3. Triplesplit Harmonie (Grundton, Quinte, Oktave)
    split_1 = phase_sharp
    split_2 = np.sin(2 * np.pi * (freq_base * 1.498) * t + np.pi/3)  # Just Fifth
    split_3 = np.sin(2 * np.pi * (freq_base * 2.000) * t + 2*np.pi/3) # Octave
    
    raw_triplesplit = (split_1 + 0.7 * split_2 + 0.5 * split_3) / 2.2

    # 4. Multi-Shell Chaos Injection (r-Value)
    x = 0.5 * np.ones(len(t))
    for i in range(1, len(t)):
        x[i] = chaos_r * x[i-1] * (1.0 - x[i-1])
    chaos_mod = np.interp(t, np.linspace(0, DUR, len(x)), x) - 0.5

    # 5. Fusion & Rubber Band-Filterung
    fused_signal = (raw_triplesplit + 0.2 * chaos_mod) * envelope
    
    # Dynamic Spatial Stereo Trajectory
    mix_l = fused_signal * np.cos(np.pi / 4.0 * xpi_sharpness)
    mix_r = np.roll(fused_signal, int(SR * 0.0025)) * np.sin(np.pi / 4.0 * xpi_sharpness)

    # Clean Cast
    mix_l = np.nan_to_num(mix_l)
    mix_r = np.nan_to_num(mix_r)
    m = np.max(np.abs([mix_l, mix_r]))
    if m == 0: m = 1.0

    audio_out = (np.vstack((mix_l/m, mix_r/m)).T * 32767).astype(np.int16)
    w.write(f"opt_saf_{v}.wav", SR, audio_out)

# 8 Neue Samples (v68 - v75)
config = [
    ('v68_rubber_sub_c1',        32.70,  1.0, 1.2, 3.57), # Low Deep Sub (C1)
    ('v69_rubber_root_c2',       65.41,  1.2, 1.4, 3.65), # Sub Bass (C2)
    ('v70_sharpness_fifth_g2',   98.00,  1.4, 1.6, 3.72), # Mid Low Quinte (G2)
    ('v71_sharpness_root_c3',   130.81,  1.6, 1.8, 3.80), # Mid Root (C3)
    ('v72_triplesplit_fifth_g3', 196.00,  1.8, 2.0, 3.87), # Mid High Quinte (G3)
    ('v73_triplesplit_oct_c4',   261.63,  2.0, 2.2, 3.92), # High Octave (C4)
    ('v74_max_sharpness_e4',     329.63,  2.2, 2.5, 3.96), # High Terz (E4)
    ('v75_leaps_fusion_g4',      392.00,  2.5, 3.0, 3.99)  # Max Rubber Fusion (G4)
]

for v, f_hz, xpi, rub, r_val in config:
    gen_triplesplit_rubber_saf(v, f_hz, xpi, rub, r_val)
    print(f"[Rubber Triplesplit] opt_saf_{v}.wav ({f_hz} Hz @ 96 BPM) generiert.")
