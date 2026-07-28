import numpy as np, scipy.io.wavfile as w, scipy.signal as s

SR, DUR = 44100, 10
t = np.linspace(0, DUR, SR * DUR, endpoint=False)

# Metrik: 3/4-Takt @ 96 BPM
BPM = 96.00
TRIPLET_FREQ = (BPM / 60.0) * 3 * 3  # 14.4 Hz Base

def gen_saf_4d_vectorcube(v, freq_base, hypercube_dim, spatial_depth, chaos_r):
    # 1. Vektorenwürfel Kanten-Trajektorie (3D spatial rotation in t)
    vx = np.sin(2 * np.pi * (TRIPLET_FREQ / 4.0) * t)
    vy = np.cos(2 * np.pi * (TRIPLET_FREQ / 3.0) * t)
    vz = np.sin(2 * np.pi * (TRIPLET_FREQ / 6.0) * t * hypercube_dim)

    # 2. Gespiegelter Tripleslit (Spiegelung der Phasenvektoren in 3 Frequenzbändern)
    phi_band1 = 2 * np.pi * freq_base * t + vx
    phi_band2 = 2 * np.pi * (freq_base * 1.5) * t + (np.pi - vy)  # Symmetrisch gespiegelt
    phi_band3 = 2 * np.pi * (freq_base * 2.0) * t + (np.pi / 2.0 + vz)

    wave_b1 = np.sin(phi_band1)
    wave_b2 = np.sin(phi_band2) * 0.75
    wave_b3 = np.cos(phi_band3) * 0.50

    tripleslit_mirrored = (wave_b1 + wave_b2 + wave_b3) / 2.25

    # 3. Feigenbaum-Chaos Attraktor (4D Kontinuität)
    x = 0.5 * np.ones(len(t))
    for i in range(1, len(t)):
        x[i] = chaos_r * x[i-1] * (1.0 - x[i-1])
    chaos_4d = np.interp(t, np.linspace(0, DUR, len(x)), x) - 0.5

    # 4. SAF Raum-Audio Fusion (Early Reflections & Dynamic Spatial Expansion)
    direct_signal = (tripleslit_mirrored + 0.2 * chaos_4d)
    
    # Raumkomponente über Delay-Kaskade (Hyperraum-Depth)
    delay_samples_l = int(SR * (0.012 * spatial_depth))
    delay_samples_r = int(SR * (0.019 * spatial_depth))
    
    room_l = np.roll(direct_signal, delay_samples_l) * 0.4
    room_r = np.roll(direct_signal, delay_samples_r) * 0.4

    # Stereo-Synthese aus Vektorenwürfel x/y-Koordinaten
    mix_l = (direct_signal * (1.0 + 0.5 * vx) + room_l)
    mix_r = (direct_signal * (1.0 - 0.5 * vx) + room_r)

    # Bandpass-Filterung je nach Frequenzband
    sos = s.butter(4, [max(20, freq_base * 0.7), min(20000, freq_base * 4.0)], btype='bandpass', output='sos', fs=SR)
    mix_l = s.sosfilt(sos, mix_l)
    mix_r = s.sosfilt(sos, mix_r)

    # Clean Cast & Output Normalisierung
    mix_l = np.nan_to_num(mix_l)
    mix_r = np.nan_to_num(mix_r)
    m = np.max(np.abs([mix_l, mix_r]))
    if m == 0: m = 1.0

    audio_out = (np.vstack((mix_l/m, mix_r/m)).T * 32767).astype(np.int16)
    w.write(f"opt_saf_{v}.wav", SR, audio_out)

# 8 Neue 4D-Hyperraum Samples (v84 - v91)
config = [
    ('v84_hypercube_sub_c1',     32.70,  1.0, 1.2, 3.68), # Deep 4D Sub
    ('v85_hypercube_root_c2',    65.41,  1.2, 1.5, 3.75), # Low Punch
    ('v86_mirrored_fifth_g2',    98.00,  1.4, 1.8, 3.82), # Gespiegelte Quinte
    ('v87_mirrored_root_c3',    130.81,  1.6, 2.1, 3.89), # Mid Root Space
    ('v88_tripleslit_e3',       164.81,  1.8, 2.4, 3.93), # Mid Band Waves
    ('v89_tripleslit_g3',       196.00,  2.0, 2.7, 3.96), # High Space Waves
    ('v90_4d_raum_c4',          261.63,  2.3, 3.0, 3.98), # Hyperraum Top C4
    ('v91_4d_fusion_e4',        329.63,  2.6, 3.5, 3.99)  # Full SAF Spatial Fusion
]

for v, f_hz, cube_d, space_d, r_val in config:
    gen_saf_4d_vectorcube(v, f_hz, cube_d, space_d, r_val)
    print(f"[4D Hypercube SAF] opt_saf_{v}.wav ({f_hz} Hz @ 96 BPM) generiert.")
