import math, struct, wave
r = 3.57 
x = 0.5
phase = 0
wav = wave.open('saf_full_chaos.wav', 'w')
wav.setnchannels(1)
wav.setsampwidth(2)
wav.setframerate(44100)
for i in range(44100 * 60):
    x = r * x * (1 - x)
    freq = 30 * (22000/30)**x
    wobble = 0.5 + 0.5 * math.sin(i / 2000)
    phase += 2 * math.pi * freq / 44100
    sample = int(math.sin(phase) * (32767 * wobble))
    wav.writeframes(struct.pack('h', sample))
wav.close()
