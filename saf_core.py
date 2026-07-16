import math, struct, wave, sys
from lebensinseln_core import get_fusion_vector

def gen(m, tree_type='Eiche'):
    fusion_vec = get_fusion_vector(tree_type, 1.0)
    m_dynamic = min(max(m * fusion_vec[0], 0.0), 1.0)
    
    wav = wave.open('saf_output.wav', 'w')
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(44100)
    
    for i in range(44100 * 5):
        t = i / 44100
        techno = (math.sin(2 * math.pi * 40 * t) * (i % 8000 < 1000))
        ambient = math.sin(2 * math.pi * 40 * t) * (0.5 + 0.5 * math.sin(2 * math.pi * 0.5 * t))
        out = (1 - m_dynamic) * techno + m_dynamic * ambient
        wav.writeframes(struct.pack('h', int(out * 30000)))
    
    wav.close()
    print(f"Fusion erfolgreich mit Baum: {tree_type} | m_dynamic: {m_dynamic:.2f}")

if __name__ == "__main__":
    morph = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
    tree = sys.argv[2] if len(sys.argv) > 2 else 'Eiche'
    gen(morph, tree)

