import os, time, math, subprocess
from prime_stream import get_prime_jump

r_file = 'saf_data/r_val'
if not os.path.exists('saf_data'): os.makedirs('saf_data')

# Initialisiere den SoX-Audiostream (streamt rohe Daten an die Soundkarte)
# Wir erzeugen eine Sample-Rate von 44100 Hz, Mono, 16-bit
sox_cmd = ['play', '-r', '44100', '-b', '16', '-c', '1', '-t', 'raw', '-']
sox_process = subprocess.Popen(sox_cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

phase = 0
iteration_index = 0
print("Starte akustische Synthese... (Hörbares Chaos)")

while True:
    # Lese den aktuellen r-Wert (die "Fahrt")
    r = 3.0 # Standard
    if os.path.exists(r_file):
        try:
            with open(r_file, 'r') as fr:
                c = fr.read().strip()
                if c: r = float(c)
        except: pass
    
    # Berechne den chaotischen Zustand (Iteriere die logistische Abbildung)
    x = 0.5
    for i in range(50): x = r * x * (1 - x) # Warm-up
    
    # Dies ist dein chaotischer Wert (Attraktor-Punkt)
    x_attractor = r * x * (1 - x)
    
    # -- Synthese-Logik --
    # Wir interpretieren den chaotischen Wert als Frequenz-Modulator
    # Basis-Frequenz: 220 Hz (A3)
    base_freq = 220 + (x_attractor * 440) # Moduliert um eine Oktave
    
    # Erzeuge Sinus-Welle für das aktuelle Zeitfenster
    # Wir erzeugen 100 Samples pro r-Schritt
    chunk_size = 100
    audio_chunk = bytearray()
    for i in range(chunk_size):
        phase += 2 * math.pi * base_freq / 44100
        sample = int(math.sin(phase) * 32767)
        audio_chunk.extend(sample.to_bytes(2, byteorder='little', signed=True))
    
    # Sende das Audio-Chunk an den SoX-Prozess
    sox_process.stdin.write(audio_chunk)
    
    # Wende die Primzahl-Logik an (für die Architektur)
    get_prime_jump(iteration_index)
    
    iteration_index += 1
    time.sleep(0.01) # Takt der Synthese
