import math, wave, struct

# Konfiguration
filename = 'chaotic_dna_safe.wav'
sample_rate = 44100
duration = 5 # Sekunden
num_samples = sample_rate * duration

wav_file = wave.open(filename, 'w')
wav_file.setnchannels(1)
wav_file.setsampwidth(2)
wav_file.setframerate(sample_rate)

r = 3.57 
x = 0.5
phase = 0

print("Generiere chaotische DNA...")
for i in range(num_samples):
    # Logistische Abbildung
    x = r * x * (1 - x)
    
    # Frequenzmodulation
    freq = 110 + (x * 440)
    phase += 2 * math.pi * freq / sample_rate
    
    # Wellenform in Bytes packen
    sample = int(math.sin(phase) * 32767)
    wav_file.writeframes(struct.pack('h', sample))
    
    if i % (sample_rate) == 0: print(f"Sekunde {i//sample_rate} fertig.")

wav_file.close()
print(f"Fertig! Datei: {filename}")
