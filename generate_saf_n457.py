import numpy as np
from scipy.io import wavfile

# Common Grid Setup: 87.2727... BPM = 960/11 BPM (32 Beats = 22.0 Seconds)
bpm = 960.0 / 11.0
sample_rate = 44100
duration = 22.0
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
sixteenth_dur = (60.0 / bpm) / 4.0
pi_2 = np.pi / 2.0

def get_env(pattern="straight"):
    env = np.zeros_like(t)
    for i in range(128):
        idx = int(np.round(i * sixteenth_dur * sample_rate))
        if pattern == "straight":
            amp = 1.0 if i % 4 == 0 else (0.5 if i % 2 == 0 else 0.25)
            decay = 0.10
        elif pattern == "offbeat":
            amp = 1.0 if i % 4 == 2 else 0.3
            decay = 0.07
        elif pattern == "rolling":
            amp = 0.9 if i % 2 == 0 else 0.4
            decay = 0.05
        elif pattern == "staccato":
            amp = 1.0 if i % 4 == 0 else 0.6
            decay = 0.03
        elif pattern == "polyrhythmic":
            amp = 1.0 if i % 3 == 0 else 0.25
            decay = 0.08
        elif pattern == "halftime":
            amp = 1.0 if i % 8 == 0 else (0.4 if i % 4 == 0 else 0.1)
            decay = 0.18
        elif pattern == "dense":
            amp = 1.0 if i % 2 == 0 else 0.6
            decay = 0.04
        elif pattern == "ambient":
            amp = 1.0 if i % 16 == 0 else 0.3
            decay = 0.35
            
        t_e = t[idx:] - (i * sixteenth_dur)
        e = amp * np.exp(-t_e / decay)
        len_add = min(len(e), len(t) - idx)
        env[idx:idx + len_add] += e[:len_add]
    return np.tanh(env)

# --- MANDELBROT WEIGHTS GENERATION (N=457) ---
N_457 = 457
c_vals = np.linspace(-2.0 + 0.1j, 0.5 + 0.6j, N_457)
mandel_weights = np.zeros(N_457)

for idx, c in enumerate(c_vals):
    z = 0
    for iter_step in range(30):
        z = z*z + c
        if abs(z) > 2.0:
            mandel_weights[idx] = iter_step / 30.0
            break
    else:
        mandel_weights[idx] = 1.0

mandel_weights /= (np.arange(1, N_457 + 1) ** 0.6)
mandel_weights /= np.sum(mandel_weights)
active_indices = np.argsort(mandel_weights)[-64:]

# Synthese
s13 = sum(mandel_weights[k] * np.sin(2 * np.pi * (55.0 * (1 + k/16.0)) * t + (k % 4) * pi_2) for k in active_indices) * get_env("straight")

sweep = np.sin(2 * np.pi * (bpm/60.0/4.0) * t) * pi_2
s14 = sum(mandel_weights[k] * np.sin(2 * np.pi * (110.0 * (1 + k/457.0)) * t + sweep + (k * pi_2 / 2)) for k in active_indices[:32]) * get_env("offbeat")

ts_core = (np.sin(2*np.pi*110*t) + np.sin(2*np.pi*110*t + pi_2) + np.sin(2*np.pi*110*t + 2*pi_2)) / 3.0
frac_457 = sum((1.0 / (k ** 0.5)) * np.cos(2 * np.pi * (55.0 * (1 + k/457.0)) * t + pi_2) for k in range(1, 457, 7))
s15 = (ts_core * 0.5 + frac_457 * 0.5) * get_env("rolling")

s16 = sum(np.sin(2 * np.pi * (43.65 * (1 + (k / 457.0) * 8.0)) * t + (k % 2) * pi_2) for k in range(1, 16)) * get_env("halftime")

mod_5d = np.sin(2 * np.pi * (bpm/60.0) * t) * np.cos(2 * np.pi * (bpm/60.0 * 3) * t + pi_2)
s17 = sum((1.0 / np.log(k + 2)) * np.sin(2 * np.pi * (110.0 + k * 0.5) * t * (1 + 0.02 * mod_5d)) for k in range(1, 457, 13)) * get_env("staccato")

s18 = sum(np.sin(2 * np.pi * (220.0 * (1 + k/457.0)) * t + pi_2) for k in range(1, 457, 16)) * np.cos(2 * np.pi * (bpm/30.0) * t + pi_2) * get_env("polyrhythmic")

s19 = sum(np.sin(2 * np.pi * (110.0 * (1 + k * 16 / 457.0)) * t + pi_2) * np.cos(2 * np.pi * (165.0 * (1 + k * 16 / 457.0)) * t + pi_2) for k in range(1, 32)) * get_env("dense")

s20 = sum((mandel_weights[k] if k < len(mandel_weights) else 1.0/k) * np.sin(2 * np.pi * (55.0 * (1 + k/16.0)) * t + (k % 4) * pi_2) for k in range(1, 457, 5)) * (0.3 + 0.7 * get_env("ambient"))

# Schreiben der sauberen WAV-Dateien (ohne korrupte Header)
signals = [s13, s14, s15, s16, s17, s18, s19, s20]
for idx, sig in enumerate(signals, start=13):
    sig /= np.max(np.abs(sig))
    filename = f"SAF_Var{idx}_STELLAR_N457.wav"
    wavfile.write(filename, sample_rate, (sig * 32767).astype(np.int16))

print("[SAF SYSTEM] 8 x saubere PCM-WAV Dateien neu generiert!")
