import numpy as np, scipy.io.wavfile as w, scipy.signal as s

SR, DUR = 44100, 10
t = np.linspace(0, DUR, SR * DUR, endpoint=False)

# Metrik: 3/4-Takt @ 96 BPM / 192 BPM Modulationsraster
BPM = 96.00
TRIPLET_FREQ = (BPM / 60.0) * 3 * 3

# Feigenbaum-Konstanten
FEIGENBAUM_DELTA = 4.669201609102990
FEIGENBAUM_ALPHA = 2.502907875095892

def gen_saf_5d_juliafield(v, freq_base, spatial_5d_depth, chaos_r):
    # 1. 5D-Vektor-Rotation (x, y, z, w, v) auf Tripleslit
    v_x = np.sin(2 * np.pi * (TRIPLET_FREQ / 3.0) * t)
    v_y = np.cos(2 * np.pi * (TRIPLET_FREQ / 4.0) * t)
    v_z = np.sin(2 * np.pi * (TRIPLET_FREQ / 6.0) * t * FEIGENBAUM_ALPHA)
    v_w = np.cos(2 * np.pi * (TRIPLET_FREQ / 8.0) * t / FEIGENBAUM_DELTA)
    v_v = np.sin(2 * np.pi * (TRIPLET_FREQ / 12.0) * t * spatial_5d_depth)

    # 2. Tripleslit 5D Cross-Phase Modulation
    phi1 = 2 * np.pi * freq_base * t + v_x + v_w
    phi2 = 2 * np.pi * (freq_base * 1.50) * t + (np.pi / 3.0) + v_y - v_v
    phi3 = 2 * np.pi * (freq_base * 2.00) * t + (2 * np.pi / 3.0) + v_z

    core_5d = (np.sin(phi1) + 0.85 * np.sin(phi2) + 0.65 * np.cos(phi3)) / 2.5

    # 3. Juliafields Quaternions / 5D-Attraktor
    # Chaos-Attraktor an Bifurkationspunkten moduliert
    x = 0.5 * np.ones(len(t))
    for i in range(1, len(t)):
        x[i] = chaos_r * x[i-1] * (1.0 - x[i-1])
    chaos_5d = np.interp(t, np.linspace(0, DUR, len(x)), x) - 0.5

    # 4. Spatial 5D Dynamic Pan & Multi-Tap Dispersion
    raw_mix = core_5d + 0.25 * chaos_5d
    
    del_1 = int(SR * 0.008 * spatial_5d_depth)
    del_2 = int(SR * 0.017 * spatial_5d_depth)
    del_3 = int(SR * 0.029 * spatial_5d_depth)

    mix_l = raw_mix * (1.0 + 0.5 * v_x) + np.roll(raw_mix, del_1) * 0.4 - np.roll(raw_mix, del_3) * 0.2
    mix_r = raw_mix * (1.0 - 0.5 * v_x) + np.roll(raw_mix, del_2) * 0.4 + np.roll(raw_mix, del_3) * 0.2

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

# 8 Neue 5D-Juliafield Samples (v108 - v115)
config = [
    ('v108_5d_sub_c0',         16.35,  1.5, 3.85), # Sub 5D Ground C0
    ('v109_5d_bass_c1',        32.70,  2.0, 3.91), # Deep Bass C1
    ('v110_julia_root_c2',     65.41,  2.5, 3.95), # Juliafield Punch C2
    ('v111_julia_fifth_g2',    98.00,  3.0, 3.97), # Spiral Fifth G2
    ('v112_5d_mid_c3',        130.81,  3.5, 3.98), # Hyper Mid C3
    ('v113_5d_terz_e3',       164.81,  4.0, 3.99), # Spatial Terz E3
    ('v114_julia_high_c4',    261.63,  4.5, 3.995),# Spiral High C4
    ('v115_julia_apex_c5',    523.25,  5.0, 3.999) # 5D Singularity Top C5
]

for v, f_hz, s_depth, r_val in config:
    gen_saf_5d_juliafield(v, f_hz, s_depth, r_val)
    print(f"[5D Juliafield SAF] opt_saf_{v}.wav ({f_hz} Hz @ 96/192 BPM) generiert.")
