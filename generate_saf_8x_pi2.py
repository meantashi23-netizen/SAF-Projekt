import numpy as np
from scipy.io import wavfile

# Grid Settings: 87.2727... BPM = 960/11 BPM (32 Beats = 22.0 Seconds)
bpm = 960.0 / 11.0
sample_rate = 44100
duration = 22.0
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
sixteenth_dur = (60.0 / bpm) / 4.0
pi_2 = np.pi / 2.0

def get_env(pattern="straight"):
    env = np.zeros_like(t)
    for i in range(128):
        idx = int(i * sixteenth_dur * sample_rate)
        amp = 1.0 if (i % 4 == 0 if pattern in ["straight", "staccato"] else i % 4 == 2) else 0.4
        decay = 0.03 if pattern == "staccato" else (0.05 if pattern == "rolling" else 0.10)
        t_e = t[idx:] - (i * sixteenth_dur)
        e = amp * np.exp(-t_e / decay)
        len_add = min(len(e), len(t) - idx)
        env[idx:idx + len_add] += e[:len_add]
    return np.tanh(env)

# Var 5: Orthogonal Tripleslit
w1, w2, w3 = np.sin(2*np.pi*110*t), np.sin(2*np.pi*110*t + pi_2), np.sin(2*np.pi*110*t + 2*pi_2)
s5 = ((w1+w2+w3)/3.0) * (0.3 + 0.7*get_env("straight"))

# Var 6: Fractal Quadrature
s6 = sum((1.0/n)*(np.sin(2*np.pi*110*(1+n/16.0)*t) + np.cos(2*np.pi*110*(1+n/16.0)*t + pi_2)) for n in range(1,17)) * get_env("offbeat")

# Var 7: Omakoma 5D Fold
s7 = np.sin(2*np.pi*55*t) * (1 + 0.5*np.sin(2*np.pi*(bpm/60)*t)*np.cos(2*np.pi*(bpm/30)*t + pi_2)) * get_env("rolling")

# Var 8: Sub Inverted
s8 = (np.sin(2*np.pi*43.65*t) + np.sin(2*np.pi*43.65*t + pi_2)) * get_env("straight")

# Var 9: Hilbert High Band
s9 = np.sin(2*np.pi*220*t) * np.cos(2*np.pi*(bpm/30)*t + pi_2) * get_env("staccato")

# Var 10: 5D Complex Node
s10 = sum(np.sin(2*np.pi*(110*k/2.0)*t + (k*pi_2)) for k in range(1,6)) * get_env("rolling")

# Var 11: Crossfold Tripleslit
s11 = (np.sin(2*np.pi*110*t + pi_2) * np.cos(2*np.pi*165*t + pi_2) + np.sin(2*np.pi*220*t + pi_2)) * get_env("offbeat")

# Var 12: Full Spectrum Omakoma
s12 = sum((1.0/n)*np.sin(2*np.pi*55*n*t + (n%2)*pi_2) for n in range(1,17)) * get_env("straight")

for idx, sig in enumerate([s5, s6, s7, s8, s9, s10, s11, s12], start=5):
    sig /= np.max(np.abs(sig))
    wavfile.write(f"SAF_Var{idx}_Pi2.wav", sample_rate, (sig * 32767).astype(np.int16))

print("[SAF SYSTEM] 8 x pi/2 Varianten gerendert.")
