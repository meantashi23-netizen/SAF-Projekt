import numpy as np, scipy.io.wavfile as w, scipy.signal as s
SR, DUR = 44100, 10
t = np.linspace(0, DUR, SR * DUR, endpoint=False)
t_corr = 1.00239

def gen_fusion_saf(v, bass_base, r_chaos, drive):
    # 1. Dual-Split Bifurkation mit Time-Correction (aus saf_split.py)
    x = 0.5 * np.ones(len(t)) + (0.01 * np.cos(t_corr))
    for i in range(1, len(t)):
        x[i] = r_chaos * x[i-1] * (1.0 - x[i-1])
    
    # 2. Bass-Modulation 30-150Hz + Sägezahn/Sub (aus saf_bass_synth.py)
    base_freq = bass_base + (x * 120.0)
    phase = np.cumsum(base_freq / SR)
    saw_harmonics = (phase % 1) * 2.0 - 1.0  # Sägezahn Modulo
    sub_bass = np.sin(2.0 * np.pi * (base_freq / 2.0) * t)  # Sub 1 Oktave tiefer
    
    raw_bass = saw_harmonics + (0.5 * sub_bass)
    
    # 3. Röhren-Sättigung / Distortion Symmetrie
    saturated = np.tanh(raw_bass * drive)
    
    # 4. SAF Spatial Stereo Split
    b, a = s.butter(3, [40/(SR/2), 3500/(SR/2)], 'band')
    clean_audio = s.lfilter(b, a, saturated)
    
    mix_l = clean_audio * np.cos(2 * np.pi * 0.2 * t)
    mix_r = np.roll(clean_audio, 128) * np.sin(2 * np.pi * 0.2 * t)
    
    m = np.max(np.abs([mix_l, mix_r]))
    w.write(f"opt_saf_{v}.wav", SR, (np.vstack((mix_l/m, mix_r/m)).T * 32767).astype(np.int16))

for v, f_b, r_val, drv in [
    ('v44_dual_split_bass', 30.0, 3.57, 1.8),
    ('v45_moog_chaos_saturate', 45.0, 3.78, 2.5),
    ('v46_tcorr_sub_drive', 60.0, 3.89, 3.2),
    ('v47_max_fusion_tube', 75.0, 3.99, 4.5)
]:
    gen_fusion_saf(v, f_b, r_val, drv)
    print(f"[SAF Fusion] opt_saf_{v}.wav (Frequency Base: {f_b}Hz, Drive: {drv}) generiert.")
