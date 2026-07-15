import numpy as np
import wave, struct

def generate_fast_morph(filename, morph=0.5, duration_sec=10):
    sr = 44100
    t = np.linspace(0, duration_sec, sr * duration_sec)
    
    # Chaos-Signal (r=3.57)
    # Wir vereinfachen die Iteration, da für Audio kurze Abschnitte reichen
    x = 0.5 + 0.1 * np.sin(2 * np.pi * 5 * t)
    
    # Profile
    techno = np.sin(2 * np.pi * 40 * t) * (t % 0.2 < 0.05)
    ambient = np.sin(2 * np.pi * 40 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.1 * t))
    
    output = (1 - morph) * techno + (morph * ambient)
    output = (output * 32767).astype(np.int16)
    
    with wave.open(filename, 'wb') as wav:
        wav.setnchannels(1); wav.setsampwidth(2); wav.setframerate(sr)
        wav.writeframes(output.tobytes())

generate_fast_morph('saf_morph_output.wav', morph=0.5)
