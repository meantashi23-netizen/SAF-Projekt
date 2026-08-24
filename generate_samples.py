import numpy as np
import wave

sample_rate = 44100
duration = 11.0
feigenbaum_alpha = 4.6692016091
base_freqs = [110.0, 146.83, 196.0]

t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

for idx, base_freq in enumerate(base_freqs, start=1):
    if idx == 1:
        intervals = [1.0, 1.25, 1.5, 1.875]
    elif idx == 2:
        intervals = [1.0, 1.333, 1.618, 2.0]
    else:
        intervals = [1.0, 1.2, 1.4, 1.6, 1.8]

    audio_signal = np.zeros_like(t)
    for ratio in intervals:
        freq = base_freq * ratio
        phase_mod = np.sin(2 * np.pi * (freq / feigenbaum_alpha) * t)
        audio_signal += np.sin(2 * np.pi * freq * t + phase_mod) / len(intervals)

    envelope = np.ones_like(t)
    fade_len = int(sample_rate * 0.1)
    envelope[:fade_len] = np.linspace(0, 1, fade_len)
    envelope[-fade_len:] = np.linspace(1, 0, fade_len)
    audio_signal *= envelope

    audio_signal /= np.max(np.abs(audio_signal))
    audio_int16 = (audio_signal * 32767).astype(np.int16)

    filename = f"SAF_Sample_0{idx}_11s_87bpm.wav"
    with wave.open(filename, 'w') as wav_file:
        wav_file.setparams((1, 2, sample_rate, len(t), 'NONE', 'not compressed'))
        wav_file.writeframes(audio_int16.tobytes())
    print(f"Erstellt: {filename}")

