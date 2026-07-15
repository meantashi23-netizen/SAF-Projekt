import math, struct, wave, sys

def gen(m):
    wav = wave.open('saf_morph.wav', 'w')
    wav.setnchannels(1); wav.setsampwidth(2); wav.setframerate(44100)
    # Techno=0.0, Ambient=1.0
    for i in range(44100 * 5): # 5 Sekunden reichen für Performance
        t = i / 44100
        # Oszillator + Morphing-Logik ohne Numpy
        techno = (math.sin(2 * math.pi * 40 * t) * (i % 8000 < 1000))
        ambient = math.sin(2 * math.pi * 40 * t) * (0.5 + 0.5 * math.sin(2 * math.pi * 0.5 * t))
        out = (1 - m) * techno + m * ambient
        wav.writeframes(struct.pack('h', int(out * 30000)))
    wav.close()

if __name__ == "__main__":
    gen(float(sys.argv[1]))
