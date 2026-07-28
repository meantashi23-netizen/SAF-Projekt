import numpy as np, scipy.io.wavfile as w, scipy.signal as s

SR, DUR = 44100, 10
t = np.linspace(0, DUR, SR * DUR, endpoint=False)

# Metrik: 3/4-Takt @ 96 BPM (14.4 Hz Base) & 192 BPM Harmonisierung
BPM = 96.00
TRIPLET_FREQ = (BPM / 60.0) * 3 * 3

def gen_saf_apex_singularity(v, freq_base, hyper_rot, spatial_span, chaos_r):
    # 1. Apex Dynamic Triplesplit & Cross-Phase Mod
    phi1 = 2 * np.pi * freq_base * t
    phi2 = 2 * np.pi * (freq_base * 1.50) * t + hyper_rot * np.sin(2 * np.pi * TRIPLET_FREQ * t)
    phi3 = 2 * np.pi * (freq_base * 2.00) * t + hyper_rot * np.cos(2 * np.pi * TRIPLET_FREQ * t)

    core_signal = (np.sin(phi1) + 0.8 * np.sin(phi2) + 0.6 * np.cos(phi3)) / 2.4

    # 2. Chaos Attraktor Singularität (Edge of Chaos)
    x = 0.5 * np.ones(len(t))
    for i in range(1, len(t)):
        x[i] = chaos_r * x[i-1] * (1.0 - x[i-1])
    chaos_apex = np.interp(t, np.linspace(0, DUR, len(x)), x) - 0.5

    # 3. 4D Spatial Audio Fusion Matrix (Hypercube Stereo Engine)
    pan_l = np.cos(2 * np.pi * (TRIPLET_FREQ / 3.0) * t + hyper_rot)
    pan_r = np.sin(2 * np.pi * (TRIPLET_FREQ / 3.0) * t + hyper_rot)

    # Multi-Tap Delay Faltung für maximale Raumtiefe
    delay_l = int(SR * 0.011 * spatial_span)
    delay_r = int(SR * 0.023 * spatial_span)

    raw_mix = core_signal + 0.2 * chaos_apex
    
    mix_l = raw_mix * (1.0 + 0.4 * pan_l) + np.roll(raw_mix, delay_l) * 0.3
    mix_r = raw_mix * (1.0 + 0.4 * pan_r) + np.roll(raw_mix, delay_r) * 0.3

    # Dynamic Bandpass Filtering
    sos = s.butter(4, [max(16, freq_base * 0.5), min(20000, freq_base * 5.0)], btype='bandpass', output='sos', fs=SR)
    mix_l = s.sosfilt(sos, mix_l)
    mix_r = s.sosfilt(sos, mix_r)

    # Clean Cast & Output Normalisierung
    mix_l = np.nan_to_num(mix_l)
    mix_r = np.nan_to_num(mix_r)
    m = np.max(np.abs([mix_l, mix_r]))
    if m == 0: m = 1.0

    audio_out = (np.vstack((mix_l/m, mix_r/m)).T * 32767).astype(np.int16)
    w.write(f"opt_saf_{v}.wav", SR, audio_out)

# 8 Finale Apex Samples (v100 - v107)
config = [
    ('v100_apex_sub_c0',        16.35,  0.5, 1.2, 3.80), # Sub Ground Zero C0
    ('v101_apex_bass_c1',       32.70,  1.0, 1.6, 3.88), # Deep Bass C1
    ('v102_apex_punch_c2',      65.41,  1.5, 2.0, 3.93), # Low Punch C2
    ('v103_apex_fifth_g2',      98.00,  2.0, 2.4, 3.96), # Resonant Quinte G2
    ('v104_apex_mid_c3',       130.81,  2.5, 2.8, 3.98), # Hyper Mid C3
    ('v105_apex_terz_e3',      164.81,  3.0, 3.2, 3.99), # Spatial Terz E3
    ('v106_apex_high_c4',      261.63,  3.5, 3.6, 3.999),# High Singularity C4
    ('v107_apex_top_c5',       523.25,  4.0, 4.0, 3.999) # Apex Top Beam C5
]

for v, f_hz, h_rot, s_span, r_val in config:
    gen_saf_apex_singularity(v, f_hz, h_rot, s_span, r_val)
    print(f"[SAF Apex] opt_saf_{v}.wav ({f_hz} Hz @ 96/192 BPM) generiert.")
