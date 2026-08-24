import numpy as np, scipy.io.wavfile as w, scipy.signal as s
SR, DUR = 44100, 10
t = np.linspace(0, DUR, SR * DUR, endpoint=False)

def gen_symbiosis(v, f_base, symbiosis_val, feig_r, mod_f):
    S = np.clip(symbiosis_val / 999.0, 0.0, 0.999)
    x = 0.5 * np.ones(len(t))
    for i in range(1, len(t)): x[i] = feig_r * x[i-1] * (1 - x[i-1])
    b, a = s.butter(3, [800/(SR/2), 4000/(SR/2)], 'band')
    chaos = s.lfilter(b, a, x - np.mean(x))
    
    carrier = np.sin(2 * np.pi * f_base * t)
    symb_carrier = (1 - S) * carrier + S * (carrier * chaos * 2)
    mod = 0.5 * (1 + np.sin(2 * np.pi * mod_f * t))
    
    mix_l = (symb_carrier * mod) + (chaos * (0.05 + 0.2 * S))
    mix_r = (np.cos(2 * np.pi * f_base * t * (1 + 0.01 * S)) * mod) + (np.roll(chaos, int(100 + 400 * S)) * (0.05 + 0.2 * S))
    m = np.max(np.abs([mix_l, mix_r]))
    w.write(f"opt_saf_{v}.wav", SR, (np.vstack((mix_l/m, mix_r/m)).T * 32767).astype(np.int16))

for v, f, s_val, r, mf in [('v36_symb_111', 146.83, 111, 3.75, 4.0), ('v37_symb_333', 220.00, 333, 3.85, 8.0), ('v38_symb_666', 329.63, 666, 3.92, 12.0), ('v39_symb_999', 440.00, 999, 3.99, 16.0)]:
    gen_symbiosis(v, f, s_val, r, mf); print(f"[SAF] opt_saf_{v}.wav (Symbiose {s_val}/999) generiert.")
