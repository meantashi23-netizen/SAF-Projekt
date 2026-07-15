import math, struct, wave

def generate_loop(filename, duration_sec=60, sample_rate=44100):
    wav = wave.open(filename, 'w')
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(sample_rate)
    
    # r-Wert im chaotischen Bereich (für den "Bifurkations-Sound")
    r = 3.57 
    x = 0.5
    phase = 0
    
    for i in range(sample_rate * duration_sec):
        # Logistische Iteration
        x = r * x * (1 - x)
        
        # Frequenzmodulation (zwischen 100Hz und 500Hz für "tiefes" Chaos)
        freq = 100 + (x * 400)
        
        # Oszillator mit Phasen-Smoothing
        phase += 2 * math.pi * freq / sample_rate
        sample = int(math.sin(phase) * 32767)
        wav.writeframes(struct.pack('h', sample))
        
    wav.close()
    print(f"Loop-Datei {filename} generiert.")

generate_loop('saf_chaos_loop_60s.wav')
