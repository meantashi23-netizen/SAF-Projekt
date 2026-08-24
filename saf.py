import numpy as np
import wave

SAMPLE_RATE = 44100
DURATION = 11.0  # Exakt auf die 11-Sekunden-Struktur angepasst
FEIGENBAUM_ALPHA = 4.6692016091

base_freq = 110.0
intervals = [1.0, 1.25, 1.5, 1.61803398875]
frequencies = [base_freq * r for r in intervals]

num_samples = int(SAMPLE_RATE * DURATION)
t = np.linspace(0, DURATION, num_samples, endpoint=False)
audio_signal = np.zeros(num_samples)

for freq in frequencies:
    phase_mod = np.sin(2 * np.pi * (freq / FEIGENBAUM_ALPHA) * t)
    audio_signal += np.sin(2 * np.pi * freq * t + phase_mod)

audio_signal /= np.max(np.abs(audio_signal))
audio_int16 = (audio_signal * 32767).astype(np.int16)

with wave.open("SAF_11s_87bpm.wav", 'w') as f:
    f.setparams((1, 2, SAMPLE_RATE, num_samples, 'NONE', 'not compressed'))
    f.writeframes(audio_int16.tobytes())

print("SAF_11s_87bpm.wav erfolgreich erstellt!")
