import math, struct, wave

def generate_bass_chaos(filename, duration_sec=60):
    wav = wave.open(filename, 'w')
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(44100)
    
    r = 3.57 
    x = 0.5
    phase = 0
    
    for i in range(44100 * duration_sec):
        x = r * x * (1 - x)
        
        # Bass-Frequenz: 30Hz - 150Hz
        base_freq = 30 + (x * 120)
        
        # Sägezahn-Wellenform (Moog-esque harmonics)
        # Erzeugt durch die Modulo-Phase
        sample = int((((i * base_freq / 44100) % 1) * 2 - 1) * 20000)
        
        # Sub-Bass Addition (Sinus 1 Oktave tiefer)
        sub = int(math.sin(i * (base_freq/2) * 2 * math.pi / 44100) * 10000)
        
        # Clipping/Sättigung für den "Röhren"-Sound
        output = max(-32767, min(32767, sample + sub))
        wav.writeframes(struct.pack('h', output))
        
    wav.close()
    print("Bass-Chaos-Loop erstellt.")

generate_bass_chaos('saf_bass_chaos.wav')
