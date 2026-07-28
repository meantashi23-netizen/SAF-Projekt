import numpy as np, scipy.io.wavfile as w, scipy.signal as s

SR, DUR = 44100, 10
t = np.linspace(0, DUR, SR * DUR, endpoint=False)

# Metrik: 3/4-Takt @ 96 BPM (14.4 Hz Base)
BPM = 96.00
TRIPLET_FREQ = (BPM / 60.0) * 3 * 3

def gen_mandelbrot_inversion_saf(v, freq_base, inv_phase, spatial_room, chaos_r):
    # 1. Triplesplit Basis mit Inversions-Vektor (-n Wave)
    phi1 = 2 * np.pi * freq_base * t
    phi2 = 2 * np.pi * (freq_base * 1.4983) * t + (inv_phase * np.pi) # Antagonist-Phase
    phi3 = 2 * np.pi * (freq_base * 2.0000) * t - (inv_phase * np.pi / 2.0)

    # Negative Wave (-n) Inversion Matrix
    raw_wave = np.sin(phi1) - 0.7 * np.sin(phi2) + 0.5 * np.cos(phi3)

    # 2. Mandelbrot-Fraktal Hüllkurve
    # Iterationsschleife zur Berechnung der fraktalen Dämpfung
    c = 0.35 + 0.1 * np.sin(2 * np.pi * TRIPLET_FREQ * t)
    z = 0.0
    m_env = np.ones_like(t)
    for _ in range(5):
        z = z**2 + c
        m_env *= np.exp(-0.1 * np.abs(z))

    # 3. Feigenbaum-Chaos Attraktor
    x = 0.5 * np.ones(len(t))
    for i in range(1, len(t)):
        x[i] = chaos_r * x[i-1] * (1.0 - x[i-1])
    chaos_mod = np.interp(t, np.linspace(0, DUR, len(x)), x) - 0.5

    # 4. Faltung & Spatial Room Fusion
    fused_core = (raw_wave * m_env + 0.15 * chaos_mod)

    # Spatial Multi-Tap Delay Line für echten Raumklang
    tap1 = np.roll(fused_core, int(SR * 0.015 * spatial_room)) * 0.35
    tap2 = np.roll(fused_core, int(SR * 0.032 * spatial_room)) * 0.20
    
    mix_l = fused_core + tap1 - tap2  # Gegenphasiger Raumfaltungs-Anteil
    mix_r = fused_core - tap1 + tap2

    # Bandpass für organischen Sitz im Traktor Mix
    sos = s.butter(4, [max(18, freq_base * 0.6), min(20000, freq_base * 4.5)], btype='bandpass', output='sos', fs=SR)
    mix_l = s.sosfilt(sos, mix_l)
    mix_r = s.sosfilt(sos, mix_r)

    # Clean Cast & Output Normalisierung
    mix_l = np.nan_to_num(mix_l)
    mix_r = np.nan_to_num(mix_r)
    m = np.max(np.abs([mix_l, mix_r]))
    if m == 0: m = 1.0

    audio_out = (np.vstack((mix_l/m, mix_r/m)).T * 32767).astype(np.int16)
    w.write(f"opt_saf_{v}.wav", SR, audio_out)

# 8 Neue Samples (v92 - v99)
config = [
    ('v92_mandel_sub_c0',        16.35,  0.25, 1.0, 3.70), # Extreme Sub C0
    ('v93_mandel_root_c1',       32.70,  0.50, 1.3, 3.78), # Deep Bass C1
    ('v94_inversion_root_c2',    65.41,  0.75, 1.6, 3.84), # Inverted Punch C2
    ('v95_inversion_fifth_g2',   98.00,  1.00, 2.0, 3.90), # Inverted Quinte G2
    ('v96_spatial_root_c3',     130.81,  1.25, 2.4, 3.94), # Spatial Center C3
    ('v97_spatial_terz_e3',     164.81,  1.50, 2.8, 3.97), # Spatial Terz E3
    ('v98_mandel_high_c4',      261.63,  1.75, 3.2, 3.98), # High Fractal C4
    ('v99_mandel_top_a4',       440.00,  2.00, 3.8, 3.99)  # Ultra Top Space A4
]

for v, f_hz, inv_p, s_room, r_val in config:
    gen_mandelbrot_inversion_saf(v, f_hz, inv_p, s_room, r_val)
    print(f"[Mandelbrot Inversion] opt_saf_{v}.wav ({f_hz} Hz @ 96 BPM) generiert.")
