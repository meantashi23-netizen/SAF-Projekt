import numpy as np
from scipy.io import wavfile

# Grid Setup: 87.2727... BPM (960/11 BPM)
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
        if pattern == "tripleslit_alpha":
            amp = 1.0 if i % 6 == 0 else (0.6 if i % 3 == 0 else 0.2)
            decay = 0.09
        elif pattern == "tripleslit_beta":
            amp = 1.0 if i % 4 == 0 else (0.8 if i % 3 == 0 else 0.3)
            decay = 0.06
        elif pattern == "tripleslit_gamma":
            amp = 1.0 if i % 8 == 0 else (0.5 if i % 2 == 0 else 0.15)
            decay = 0.14
            
        t_e = t[idx:] - (i * sixteenth_dur)
        e = amp * np.exp(-t_e / decay)
        len_add = min(len(e), len(t) - idx)
        env[idx:idx + len_add] += e[:len_add]
    return np.tanh(env)

# --- TRIPLESLIT SYNTHESIS (VAR 21 - 23) ---

# Var 21: Tripleslit Phase Coherence (Interferenz der 3 Haupt-Peaks: 45.32, 49.88, 45.83 Hz)
psi1 = np.sin(2 * np.pi * 45.32 * t)
psi2 = np.sin(2 * np.pi * 49.88 * t + pi_2 / 2)
psi3 = np.sin(2 * np.pi * 45.83 * t + pi_2)
s21 = (psi1 + psi2 + psi3) * get_env("tripleslit_alpha")

# Var 22: OMAKOMA N=16 Spectral Fold (Bierspirale Modulation & Juliafield-Oszillation)
julia_mod = np.cos(2 * np.pi * (bpm / 60.0 * 4) * t) * 0.15
s22 = sum((1.0 / (k ** 0.6)) * np.sin(2 * np.pi * (55.0 * (1 + (k % 16) / 16.0)) * t * (1 + julia_mod) + k * (pi_2 / 3)) for k in range(1, 457, 9)) * get_env("tripleslit_beta")

# Var 23: Feigenbaum Attractor Drift (Bifurkations-Cluster mit 5D-Faltung)
fold_5d = np.sin(2 * np.pi * (4.6692 * 10) * t) * np.cos(2 * np.pi * (2.5029 * 5) * t)
s23 = sum(np.sin(2 * np.pi * (110.0 + k * 0.457) * t + fold_5d * 0.1) for k in range(1, 33)) * get_env("tripleslit_gamma")

# Rendern der 3 neuen WAV-Dateien
signals = [s21, s22, s23]
for idx, sig in enumerate(signals, start=21):
    sig /= np.max(np.abs(sig))
    filename = f"SAF_Var{idx}_STELLAR_N457.wav"
    wavfile.write(filename, sample_rate, (sig * 32767).astype(np.int16))

print("[SAF SYSTEM] Varianten 21, 22 & 23 (Tripleslit / OMAKOMA N=16) erfolgreich gerendert!")
