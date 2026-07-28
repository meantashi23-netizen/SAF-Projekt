import numpy as np, scipy.io.wavfile as w, scipy.signal as s
SR, DUR = 44100, 10
t = np.linspace(0, DUR, SR * DUR, endpoint=False)
BPM = 96.00
MOD_FREQ = (BPM / 60.0) * 2.0  # 3.2 Hz Pulse für Traktor-Sync

def gen_harmonic_saf(v, freq_base, xpi_phase, julia_depth, symb_ratio):
    # 1. Individuelle Trägerfrequenz pro Sample (Kein Einerlei mehr!)
    carrier = np.sin(2 * np.pi * freq_base * t)
    
    # 2. Julia-Field Fold Modulation
    z = (t * 0.05) + 1j * np.cos(2 * np.pi * MOD_FREQ * t)
    c = complex(-0.7269, 0.1889)
    julia_mod = np.zeros(len(t))
    for _ in range(julia_depth):
        z = np.clip(z, -2.0 - 2.0j, 2.0 + 2.0j)
        z = z**2 + c
        julia_mod += np.abs(z) % 1.0
    julia_mod = (julia_mod / float(julia_depth)) * 2.0 - 1.0

    # 3. Dynamic C4/16 Sub-Feeder & Wellenbaum Modulation
    bpm_grid = 0.5 * (1.0 + np.sin(2 * np.pi * MOD_FREQ * t))
    phase = (np.pi / 4.0) * xpi_phase * julia_mod
    
    # Wellenbaum-Synthese mit variabler Grundfrequenz
    synthesized = np.sin(2 * np.pi * freq_base * t + phase) * bpm_grid
    
    # Stereo Trajektorie & Symbiose-Mix
    mix_l = synthesized * (1.0 - 0.15 * symb_ratio)
    mix_r = np.roll(synthesized, int(SR * (0.002 + 0.001 * symb_ratio))) * (0.85 + 0.15 * symb_ratio)

    m = np.max(np.abs([mix_l, mix_r]))
    if m == 0: m = 1.0
    
    audio_out = (np.vstack((mix_l/m, mix_r/m)).T * 32767).astype(np.int16)
    w.write(f"opt_saf_{v}.wav", SR, audio_out)

# Frequenzen gestaffelt: C3 (130.81Hz), G3 (196.00Hz), C4 (261.63Hz), G4 (392.00Hz)
for v, f_hz, xpi, depth, symb in [
    ('v56_harmonic_sub_c3', 130.81, 1.000, 8,  0.25),
    ('v57_harmonic_fifth_g3', 196.00, 1.333, 12, 0.50),
    ('v58_harmonic_octave_c4', 261.63, 1.666, 16, 0.75),
    ('v59_harmonic_high_g4', 392.00, 2.000, 20, 1.00)
]:
    gen_harmonic_saf(v, f_hz, xpi, depth, symb)
    print(f"[Harmonic SAF] opt_saf_{v}.wav ({f_hz} Hz @ 96 BPM) generiert.")
