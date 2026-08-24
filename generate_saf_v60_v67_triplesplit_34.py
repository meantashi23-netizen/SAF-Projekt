import numpy as np, scipy.io.wavfile as w, scipy.signal as s

SR, DUR = 44100, 10
t = np.linspace(0, DUR, SR * DUR, endpoint=False)

# Metrik: 3/4-Takt @ 96 BPM mit Triolen-Unterteilung
BPM = 96.00
BEATS_PER_BAR = 3              # 3/4-Takt
TRIPLETS_PER_BEAT = 3          # Triolen-Raster (3 Impulses pro Beat)
TRIPLET_FREQ = (BPM / 60.0) * BEATS_PER_BAR * TRIPLETS_PER_BEAT  # 14.4 Hz Triolen-Pulsation

def gen_triplesplit_34_saf(v, freq_base, split_factor, chaos_r):
    # 1. 3/4-Takt & Triolen-Envelope (Triplets)
    triplet_pulse = 0.5 * (1.0 + np.sin(2 * np.pi * TRIPLET_FREQ * t))
    bar_accent = 0.7 + 0.3 * np.sin(2 * np.pi * (BPM / 60.0 / 4.0 * BEATS_PER_BAR) * t)
    triplets_envelope = triplet_pulse * bar_accent

    # 2. Triplesplit Bifurkation (3 Phasen-Axe: Setzpunkt aπ_2 aus Multi-Shell V1.8)
    split_1 = np.sin(2 * np.pi * freq_base * t)
    split_2 = np.sin(2 * np.pi * (freq_base * 1.5) * t + (np.pi / 3.0) * split_factor) # Quinte
    split_3 = np.sin(2 * np.pi * (freq_base * 2.0) * t + (2 * np.pi / 3.0) * split_factor) # Oktave
    
    triplesplit_core = (split_1 + split_2 + split_3) / 3.0

    # 3. SAF Chaos-Akkumulation (r-Wert Steuerung)
    x = 0.5 * np.ones(len(t))
    for i in range(1, len(t)):
        x[i] = chaos_r * x[i-1] * (1.0 - x[i-1])
    
    chaos_mod = np.interp(t, np.linspace(0, DUR, len(x)), x) - 0.5

    # 4. Synthese & Modulation
    modulated_signal = (triplesplit_core + 0.25 * chaos_mod) * triplets_envelope

    # 5. Spatiale SAF Triplesplit-Stereotrennung (3-Kanal Split auf Stereo)
    mix_l = modulated_signal * np.cos(2 * np.pi * (TRIPLET_FREQ / 3.0) * t)
    mix_r = np.roll(modulated_signal, int(SR * 0.003)) * np.sin(2 * np.pi * (TRIPLET_FREQ / 3.0) * t)

    # Clean Output Normalisierung
    mix_l = np.nan_to_num(mix_l)
    mix_r = np.nan_to_num(mix_r)
    m = np.max(np.abs([mix_l, mix_r]))
    if m == 0: m = 1.0

    audio_out = (np.vstack((mix_l/m, mix_r/m)).T * 32767).astype(np.int16)
    w.write(f"opt_saf_{v}.wav", SR, audio_out)

# 8 Samples (v60 - v67) im 3/4-Takt & Triolen-Gitter
samples_config = [
    ('v60_triplet_34_sub_c2',      65.41,  1.0, 3.57), # Low Bass (C2)
    ('v61_triplet_34_root_c3',     130.81, 1.2, 3.68), # Sub Root (C3)
    ('v62_triplet_34_fifth_g3',    196.00, 1.4, 3.75), # Quinte (G3)
    ('v63_triplet_34_octave_c4',   261.63, 1.6, 3.82), # Mid Octave (C4)
    ('v64_triplet_34_split_e4',    329.63, 1.8, 3.89), # Terz (E4)
    ('v65_triplet_34_high_g4',     392.00, 2.0, 3.93), # High Quinte (G4)
    ('v66_triplet_34_top_c5',      523.25, 2.2, 3.97), # High Top (C5)
    ('v67_triplet_34_max_fusion',  659.25, 2.5, 3.99)  # Peak Fusion (E5)
]

for v, f_hz, split_f, r_val in samples_config:
    gen_triplesplit_34_saf(v, f_hz, split_f, r_val)
    print(f"[3/4 Triplet SAF] opt_saf_{v}.wav ({f_hz} Hz @ 96 BPM Trioles) generiert.")
