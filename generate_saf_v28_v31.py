import numpy as np
from scipy.io import wavfile

# Grid Setup: 87.2727... BPM (960/11 BPM)
bpm = 960.0 / 11.0
sample_rate = 44100
duration = 22.0
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
sixteenth_dur = (60.0 / bpm) / 4.0
pi_2 = np.pi / 2.0

def get_env(pattern="final_pack"):
    env = np.zeros_like(t)
    for i in range(128):
        idx = int(np.round(i * sixteenth_dur * sample_rate))
        if pattern == "flux_ping":
            amp = 1.0 if i % 4 == 0 else (0.8 if i % 2 == 0 else 0.35)
            decay = 0.05
        elif pattern == "reverse_roll":
            amp = 0.3 if i % 4 == 0 else (0.9 if i % 2 == 0 else 0.6)
            decay = 0.15
        elif pattern == "double_delay_mesh":
            amp = 1.0 if i % 3 == 0 else (0.6 if i % 2 == 0 else 0.2)
            decay = 0.09
        else: # grand_closing
            amp = 1.0 if i % 8 == 0 else (0.7 if i % 4 == 0 else 0.4)
            decay = 0.2
            
        t_e = t[idx:] - (i * sixteenth_dur)
        e = amp * np.exp(-t_e / decay)
        len_add = min(len(e), len(t) - idx)
        env[idx:idx + len_add] += e[:len_add]
    return np.tanh(env)

# --- FINALE SAMPLE-SCHLIESSUNG (VAR 28 - 31) ---

# Var 28: Flux Reverse Transient Focus (Perfekt für Traktor Reverse / Flux Processing)
s28 = sum(np.sin(2 * np.pi * (45.32 * k) * (t**1.01)) for k in range(1, 12)) * get_env("flux_ping")

# Var 29: Double-Delay Phase Mesh (Vogelflug & Interferenz-Netzwerk)
s29 = sum((1.0 / k) * np.cos(2 * np.pi * (174.555 / 2 + k * 4.6692) * t + np.sin(t * 2)) for k in range(1, 25)) * get_env("reverse_roll")

# Var 30: Tripleslit High-Coherence Transient (Scharfe Flanken für FX-Chains)
s30 = (np.sin(2 * np.pi * 49.88 * t) * np.cos(2 * np.pi * 45.32 * t * 0.5)) * get_env("double_delay_mesh")

# Var 31: OMAKOMA N=16 Grand Finale (Volles spektrales Band 1 bis 16)
s31 = sum(np.sin(2 * np.pi * (55.0 * k) * t + (k * pi_2 / 8)) for k in range(1, 17)) * get_env("grand_closing")

# Rendern der finalen 4 WAV-Dateien
signals = [s28, s29, s30, s31]
for idx, sig in enumerate(signals, start=28):
    sig /= np.max(np.abs(sig))
    filename = f"SAF_Var{idx}_STELLAR_N457.wav"
    wavfile.write(filename, sample_rate, (sig * 32767).astype(np.int16))

print("[SAF SYSTEM] Varianten 28 bis 31 erfolgreich gerendert!")
print("[SAF SYSTEM] *** DAS 32-SAMPLE-PACK IST COMPLETT VOLL! ***")
