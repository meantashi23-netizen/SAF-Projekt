import numpy as np, scipy.io.wavfile as w, scipy.signal as s
SR, DUR = 44100, 10
t = np.linspace(0, DUR, SR * DUR, endpoint=False)

# Exakt festgenageltes Raster
TARGET_FREQ = 261.63  # C4 Grundfrequenz (Identisch für alle Decks)
BPM = 96.00
MOD_FREQ = (BPM / 60.0) * 2.0  # Synchronschlag auf 96 BPM (3.2 Hz Modulations-Takt)

def gen_locked_saf(v, xpi_phase, julia_depth, symb_ratio):
    # 1. Phasengleicher C4-Träger
    carrier = np.sin(2 * np.pi * TARGET_FREQ * t)
    
    # 2. Julia-Set Fold Modulation (Dynamische Tiefe, aber starre Frequenz)
    z = (t * 0.05) + 1j * np.cos(2 * np.pi * MOD_FREQ * t)
    c = complex(-0.7269, 0.1889)
    julia_mod = np.zeros(len(t))
    for _ in range(julia_depth):
        z = np.clip(z, -2.0 - 2.0j, 2.0 + 2.0j)
        z = z**2 + c
        julia_mod += np.abs(z) % 1.0
    julia_mod = (julia_mod / float(julia_depth)) * 2.0 - 1.0

    # 3. Striktes 96 BPM LFO-Raster (Wellenbaum-Pulse)
    bpm_grid = 0.5 * (1.0 + np.sin(2 * np.pi * MOD_FREQ * t))

    # 4. Phase-Locking & Symbiose
    phase = (np.pi / 4.0) * xpi_phase * julia_mod
    modulated_wave = np.sin(2 * np.pi * TARGET_FREQ * t + phase) * bpm_grid

    # Stereo-Synthese
    mix_l = modulated_wave * (1.0 - 0.2 * symb_ratio)
    mix_r = np.roll(modulated_wave, int(SR * 0.002)) * (0.8 + 0.2 * symb_ratio)

    m = np.max(np.abs([mix_l, mix_r]))
    if m == 0: m = 1.0
    
    audio_out = (np.vstack((mix_l/m, mix_r/m)).T * 32767).astype(np.int16)
    w.write(f"opt_saf_{v}.wav", SR, audio_out)

# Alle 4 Samples nutzen exakt $261.63 Hz$ auf 96.00 BPM Grid
for v, xpi, depth, symb in [
    ('v52_locked_c4_a', 1.0, 8, 0.25),
    ('v53_locked_c4_b', 1.333, 12, 0.50),
    ('v54_locked_c4_c', 1.666, 16, 0.75),
    ('v55_locked_c4_d', 2.0, 20, 1.00)
]:
    gen_locked_saf(v, xpi, depth, symb)
    print(f"[Locked Freq] opt_saf_{v}.wav (261.63Hz @ 96 BPM) generiert.")
