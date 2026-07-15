import math, struct, wave
# Fix auf 1.2 Hz für eine biologisch harmonische Pulsation (ca. 72 BPM)
p = 1.2 
wav = wave.open('saf.wav', 'w')
wav.setnchannels(1); wav.setsampwidth(2); wav.setframerate(44100)
for i in range(44100 * 10):
    t = i / 44100
    # Die "sanfte" Welle: Ein Sinus-Modulator, der in den Bereich 0.2 bis 1.0 regelt
    # Das wirkt nicht wie ein "Puls" von 0, sondern wie ein Atmen
    val = math.sin(2 * 3.1415 * 440 * t) * (0.6 + 0.4 * math.sin(2 * 3.1415 * p * t))
    wav.writeframes(struct.pack('h', int(val * 20000)))
wav.close()
