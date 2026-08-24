import numpy as np, scipy.io.wavfile as w, scipy.signal as s

SR, DUR = 44100, 10
t = np.linspace(0, DUR, SR * DUR, endpoint=False)

# Metrik: 3/4-Takt @ 96 BPM (14.4 Hz Base)
BPM = 96.00
TRIPLET_FREQ = (BPM / 60.0) * 3 * 3

FEIGENBAUM_DELTA = 4.669201609102990
FEIGENBAUM_ALPHA = 2.502907875095892

def gen_saf_wavelet_feedback(v, freq_base, feedback_gain, xpi_scale, chaos_r):
    # 1. 5D Spatial Trajektorie
    v_x = np.sin(2 * np.pi * (TRIPLET_FREQ / 3.0) * t)
    v_y = np.cos(2 * np.pi * (TRIPLET_FREQ / 4.0) * t)
    v_z = np.sin(2 * np.pi * (TRIPLET_FREQ / 6.0) * t * FEIGENBAUM_ALPHA)

    # 2. Tripleslit Core
    phi1 = 2 * np.pi * freq_base * t
    phi2 = 2 * np.pi * (freq_base * 1.50) * t + (np.pi / 3.0) * xpi_scale
    phi3 = 2 * np.pi * (freq_base * 2.00) * t + (2 * np.pi / 3.0) * xpi_scale

    core_signal = (np.sin(phi1) + 0.8 * np.sin(phi2) + 0.6 * np.cos(phi3)) / 2.4

    # 3. Wavelet Feedback Loop (Spektraler Feeder Matrix)
    # Iterative Rückkopplung der vergangenen Samples
    feedback_buf = np.zeros(len(t))
    delay_fb = int(SR * (0.005 * feedback_gain))
    
    # Chaos Injektion
    x = 0.5 * np.ones(len(t))
    for i in range(1, len(t)):
        x[i] = chaos_r * x[i-1] * (1.0 - x[i-1])
    chaos_mod = np.interp(t, np.linspace(0, DUR, len(x)), x) - 0.5

    # Feedback Integration
    for i in range(delay_fb, len(t)):
        feedback_buf[i] = core_signal[i] + feedback_gain * 0.4 * feedback_buf[i - delay_fb] * np.sin(xpi_scale * np.pi * chaos_mod[i])

    # 4. 5D Spatial Audio Fusion
    fused_out = core_signal + 0.5 * feedback_buf

    mix_l = fused_out * (1.0 + 0.4 * v_x) + np.roll(fused_out, int(SR * 0.012)) * 0.3
    mix_r = fused_out * (1.0 - 0.4 * v_x) + np.roll(fused_out, int(SR * 0.021)) * 0.3

    # Bandpass Filterung
    sos = s.butter(4, [max(16, freq_base * 0.5), min(20000, freq_base * 5.0)], btype='bandpass', output='sos', fs=SR)
    mix_l = s.sosfilt(sos, mix_l)
    mix_r = s.sosfilt(sos, mix_r)

    # Output Normalisierung
    mix_l = np.nan_to_num(mix_l)
    mix_r = np.nan_to_num(mix_r)
    m = np.max(np.abs([mix_l, mix_r]))
    if m == 0: m = 1.0

    audio_out = (np.vstack((mix_l/m, mix_r/m)).T * 32767).astype(np.int16)
    w.write(f"opt_saf_{v}.wav", SR, audio_out)

# 8 Neue Wavelet-Feedback Samples (v116 - v123)
config = [
    ('v116_feeder_sub_c0',      16.35,  1.2, 0.5, 3.82), # Deep Feeder Sub C0
    ('v117_feeder_bass_c1',     32.70,  1.5, 0.8, 3.88), # Wavelet Bass C1
    ('v118_wavelet_root_c2',    65.41,  1.8, 1.0, 3.92), # Resonant Root C2
    ('v119_wavelet_fifth_g2',   98.00,  2.2, 1.2, 3.95), # Wavelet Quinte G2
    ('v120_feeder_mid_c3',     130.81,  2.5, 1.5, 3.97), # Feedback Mid C3
    ('v121_feeder_terz_e3',    164.81,  2.8, 1.8, 3.98), # Feedback Terz E3
    ('v122_wavelet_high_c4',   261.63,  3.2, 2.0, 3.99), # Spatial Wavelet C4
    ('v123_wavelet_top_g5',    783.99,  3.5, 2.5, 3.999) # Apex Feedback Top G5
]

for v, f_hz, fb_g, xpi, r_val in config:
    gen_saf_wavelet_feedback(v, f_hz, fb_g, xpi, r_val)
    print(f"[Wavelet Feedback SAF] opt_saf_{v}.wav ({f_hz} Hz @ 96/192 BPM) generiert.")
