import math, struct, time

# SAF V29.3.2 Parameter
sample_rate = 44100
duration = 10 # Sekunden Fahrt
t_start = 0.51
t_end = 0.63

def generate_saf_audio():
    with open('saf_divergence.raw', 'wb') as f:
        for i in range(sample_rate * duration):
            t = t_start + (i / (sample_rate * duration)) * (t_end - t_start)
            
            # Die Bifurkations-DNA als Frequenz: 
            # Wir nutzen die logistische Abbildung, um den "Abstand" der Phasen zu modulieren
            x = math.sin(t * 2 * math.pi * 5) * math.exp(-(t-0.51)*10)
            freq = 220 + (x * 440) # A3 bis A4 Modulationsbereich
            
            # Oszillator
            phase = (i / sample_rate) * 2 * math.pi * freq
            sample = int(math.sin(phase) * 32767)
            f.write(struct.pack('h', sample))

generate_saf_audio()
