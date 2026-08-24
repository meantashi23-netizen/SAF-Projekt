import numpy as np, scipy.io.wavfile as w, scipy.signal as s
SR, DUR = 44100, 10
t = np.linspace(0, DUR, SR * DUR, endpoint=False)

def gen(v, f_base, feig_r, mod_f, phase):
    x = 0.5 * np.ones(len(t))
    for i in range(1, len(t)): x[i] = feig_r * x[i-1] * (1 - x[i-1])
    b, a = s.butter(3, [1200/(SR/2), 3500/(SR/2)], 'band')
    chaos = s.lfilter(b, a, x - np.mean(x))
    carrier = np.sin(2 * np.pi * f_base * t + phase)
    mod = 0.5 * (1 + np.sin(2 * np.pi * mod_f * t))
    mix_l = (carrier * mod) + (chaos * 0.15)
    mix_r = (np.cos(2 * np.pi * f_base * t) * mod) + (np.roll(chaos, 200) * 0.15)
    m = np.max(np.abs([mix_l, mix_r]))
    w.write(f"opt_saf_{v}.wav", SR, (np.vstack((mix_l/m, mix_r/m)).T * 32767).astype(np.int16))

for v, f, r, mf, p in [('v32_sub_xpi', 130.81, 3.82, 6.4, 0), ('v33_fold_5d', 261.63, 3.91, 13.71, np.pi/2), ('v34_bifurc_high', 523.25, 3.99, 24.0, np.pi/4), ('v35_omakoma_max', 196.00, 3.86, 196.83, np.pi)]:
    gen(v, f, r, mf, p); print(f"[SAF] opt_saf_{v}.wav generiert.")
