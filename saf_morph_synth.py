import math, struct, wave

def generate_morph_chaos(filename, morph=0.5, duration_sec=60):
    wav = wave.open(filename, 'w')
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(44100)
    
    r = 3.57; x = 0.5; phase = 0; env = 0
    
    for i in range(44100 * duration_sec):
        x = r * x * (1 - x)
        base_freq = 40 + (x * 100)
        
        # A) PERKUSSIVER TECHNO-BASS (Impuls-getrieben)
        env = env * 0.95 + (1.0 if i % 10000 == 0 else 0) * 1.0
        techno = math.sin(phase) * env
        
        # B) PSYCHEDELISCHER AMBIENT-SWEEP (LFO-Filter)
        sweep = math.sin(phase) * (0.5 + 0.5 * math.sin(i / 10000))
        
        # Morphing: Mische zwischen Techno (0.0) und Ambient (1.0)
        output = (1 - morph) * techno + (morph * sweep)
        
        phase += 2 * math.pi * base_freq / 44100
        wav.writeframes(struct.pack('h', int(output * 32767)))
        
    wav.close()
generate_morph_chaos('saf_morph_output.wav', morph=0.5) # Regler auf 0.5
