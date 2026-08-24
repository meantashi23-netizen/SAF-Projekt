import numpy as np
from scipy.io import wavfile

# Grid Setup: 87.2727... BPM (960/11 BPM)
bpm = 960.0 / 11.0
sample_rate = 44100
duration = 22.0
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
sixteenth_dur = (60.0 / bpm) / 4.0
pi_2 = np.pi / 2.0

def get_env(pattern="tripleslit"):
    env = np.zeros_like(t)
    for i in range(128):
        idx = int(np.round(i * sixteenth_dur * sample_rate))
        if pattern == "sub_texture":
            amp = 1.0 if i % 8 == 0 else (0.7 if i % 4 == 0 else 0.2)
            decay = 0.18
        elif pattern == "interfero":
            amp = 1.0 if i % 6 == 0 else (0.5 if i % 2 == 0 else 0.1)
            decay = 0.08
        elif pattern == "feigen_fold":
            amp = 1.0 if i % 4 == 0 else (0.8 if i % 3 == 0 else 0.3)
            decay = 0.12
        else:
            amp = 1.0 if i % 4 == 0 else 0.3
            decay = 0.1
            
        t_e = t[idx:] - (i * sixteenth_dur)
        e = amp * np.exp(-t_e / decay)
        len_add = min(len(e), len(t) - idx)
        env[idx:idx + len_add] += e[:len_add]
    return np.tanh(env)

# --- TRIPLESLIT DEEP EXTENSIONS (VAR 24 - 27) ---

# Var 24: Pitch-Down Sub-Resonance (Fokus auf tiefgepitchte Tripleslit-Phasen)
s24 = sum(np.sin(2 * np.pi * (22.66 + k * 1.168) * t + np.sin(k * t * 0.1)) for k in range(1, 16)) * get_env("sub_texture")

# Var 25: OMAKOMA Slow-Spin Texture (Bierspirale Modulation für extreme Stretch-Decks)
omakoma_sweep = np.sin(2 * np.pi * 0.25 * t)
s25 = sum((1.0 / np.sqrt(k)) * np.sin(2 * np.pi * (45.32 * (1 + k/16.0)) * t + omakoma_sweep) for k in range(1, 33)) * get_env("interfero")

# Var 26: 5D-Fold Tripleslit Interference (Dichte Phasen-Kollision im Sub-Bereich)
fold_mod = np.cos(2 * np.pi * 4.6692 * t) * 0.2
s26 = (np.sin(2 * np.pi * 45.32 * t * (1 + fold_mod)) + 
       np.sin(2 * np.pi * 49.88 * t) + 
       np.sin(2 * np.pi * 45.83 * t * (1 - fold_mod))) * get_env("feigen_fold")

# Var 27: Feigenbaum Deep Cluster (41 BPM-optimierter Granular-Drone)
s27 = sum(np.sin(2 * np.pi * (110.0 / (1 + k * 0.05)) * t) for k in range(1, 24)) * get_env("sub_texture")

# Rendern der 4 neuen WAV-Dateien
signals = [s24, s25, s26, s27]
for idx, sig in enumerate(signals, start=24):
    sig /= np.max(np.abs(sig))
    filename = f"SAF_Var{idx}_STELLAR_N457.wav"
    wavfile.write(filename, sample_rate, (sig * 32767).astype(np.int16))

print("[SAF SYSTEM] Varianten 24, 25, 26 & 27 erfolgreich gerendert!")
