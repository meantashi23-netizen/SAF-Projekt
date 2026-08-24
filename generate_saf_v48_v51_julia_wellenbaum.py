import numpy as np, scipy.io.wavfile as w, scipy.signal as s
SR, DUR = 44100, 10
t = np.linspace(0, DUR, SR * DUR, endpoint=False)

def gen_julia_wellenbaum_saf(v, c_real, c_imag, xpi_scale):
    # 1. SAF Chaos Synth
    r = 3.57
    x_cha = 0.5 * np.ones(len(t))
    for i in range(1, len(t)): x_cha[i] = r * x_cha[i-1] * (1.0 - x_cha[i-1])
    freq_exp = 30.0 * ((22000.0 / 30.0) ** (x_cha * 0.15))
    wobble = 0.5 + 0.5 * np.sin(t * 22.0)
    chaos_wave = np.sin(2 * np.pi * freq_exp * t) * wobble

    # 2. Julia-Set (Stabilisiert gegen Overflow)
    z = (t * 0.1) + 1j * np.sin(2 * np.pi * 0.5 * t)
    c = complex(c_real, c_imag)
    julia_mod = np.zeros(len(t))
    for _ in range(12):
        z = np.clip(z, -2.0 - 2.0j, 2.0 + 2.0j) # Begrenzung verhindert NaN/Overflow
        z = z**2 + c
        julia_mod += np.abs(z) % 1.0
    julia_mod = (julia_mod / 12.0) * 2.0 - 1.0

    # 3. C4(1/16)-Grundierung & Wellenbaum (261.63 Hz C4)
    f_c4 = 261.63
    c4_grid = np.sin(2 * np.pi * f_c4 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * (f_c4 / 16.0) * t))
    
    # 4. xπ Scaling & Phase Modulation
    phase_shift = (np.pi / 4.0) * xpi_scale
    wellenbaum_fusion = np.sin(2 * np.pi * f_c4 * t + phase_shift * julia_mod)

    # 5. Finale Summation & Stereo-Trajektorie
    mix_raw = (0.35 * c4_grid) + (0.35 * wellenbaum_fusion) + (0.3 * chaos_wave)
    mix_l = mix_raw * np.cos(phase_shift)
    mix_r = np.roll(mix_raw, int(SR * 0.005)) * np.sin(phase_shift)

    # Clean Normalisierung & Integer Cast
    mix_l = np.nan_to_num(mix_l)
    mix_r = np.nan_to_num(mix_r)
    m = np.max(np.abs([mix_l, mix_r]))
    if m == 0: m = 1.0
    
    audio_out = (np.vstack((mix_l/m, mix_r/m)).T * 32767).astype(np.int16)
    w.write(f"opt_saf_{v}.wav", SR, audio_out)

for v, cr, ci, xpi in [
    ('v48_julia_fold_c4', -0.7, 0.27015, 1.0),
    ('v49_wellenbaum_feeder', -0.8, 0.156, 1.333),
    ('v50_xpi_phase_90deg', -0.4, 0.6, 1.666),
    ('v51_coherence_max_fusion', -0.7269, 0.1889, 2.0)
]:
    gen_julia_wellenbaum_saf(v, cr, ci, xpi)
    print(f"[Julia-Wellenbaum] opt_saf_{v}.wav (xπ Scaling: {xpi}) sauber generiert.")
