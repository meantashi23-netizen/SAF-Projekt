# Verzeichnis und Dateien erzwingen
mkdir -p saf_data
echo "3.0" > saf_data/r_val
touch saf_data/saf_shared_mem
python3 saf_minimal.py
cat << 'EOF' > saf_minimal.py
import mmap, os, time
shared_mem_path = 'saf_data/saf_shared_mem'
r_file = 'saf_data/r_val'

if not os.path.exists(shared_mem_path):
    with open(shared_mem_path, 'wb') as f: f.write(b'\x00' * 1024)

with open(shared_mem_path, 'r+b') as f:
    mm = mmap.mmap(f.fileno(), 1024)
    while True:
        r = 3.0
        if os.path.exists(r_file):
            try:
                with open(r_file, 'r') as fr:
                    c = fr.read().strip()
                    if c: r = float(c)
            except: pass
        
        x = 0.5
        matrix = bytearray()
        for i in range(1024):
            x = r * x * (1 - x)
            matrix.append(int(x * 255))
        mm.seek(0); mm.write(matrix)
        time.sleep(0.05)
EOF

ps aux | grep python
cat << 'EOF' > saf_minimal.py
import mmap, os, time
shared_mem_path = 'saf_data/saf_shared_mem'
r_file = 'saf_data/r_val'
log_file = 'saf_data/saf_log.txt'

with open(shared_mem_path, 'wb') as f: f.write(b'\x00' * 1024)
with open(shared_mem_path, 'r+b') as f:
    mm = mmap.mmap(f.fileno(), 1024)
    while True:
        r = 3.0
        if os.path.exists(r_file):
            try:
                with open(r_file, 'r') as fr:
                    c = fr.read().strip()
                    if c: r = float(c)
            except: pass
        
        x = 0.5
        matrix = bytearray()
        for i in range(1024):
            x = r * x * (1 - x)
            matrix.append(int(x * 255))
        
        # Direktes Logging des Zustands
        with open(log_file, 'a') as fl:
            fl.write(f"r={r} | val_0={matrix[0]}\n")
            
        mm.seek(0); mm.write(matrix)
        time.sleep(0.05)
EOF

cat << 'EOF' > calculate_feigenbaum.py
import re
# Nur jede 100. Zeile lesen, um das Rauschen zu minimieren
data = {}
with open('saf_data/saf_log.txt', 'r') as f:
    for i, line in enumerate(f):
        if i % 100 == 0:
            m = re.search(r"r=([\d\.]+).*val_0=(\d+)", line)
            if m:
                r, val = round(float(m.group(1)), 4), int(m.group(2))
                if r not in data: data[r] = set()
                data[r].add(val)

# Bifurkationen finden
bifs = [r for r in sorted(data.keys()) if len(data[r]) > 1]
# Filtern: Nur Punkte, wo sich die Anzahl der Zustände wirklich ändert
print(f"Gefundene Bifurkations-Bereiche: {bifs[:10]}")
EOF

cat << 'EOF' > run_saf_all.sh
#!/bin/bash
# 1. Bereinigung
pkill -f python
rm -rf saf_data/
mkdir -p saf_data
touch saf_data/saf_log.txt

# 2. Kernel mit direktem Logging starten (Session 1)
echo "Start: SAF-Kernel (Logger aktiviert)..."
nohup python3 saf_minimal.py > saf_data/kernel.log 2>&1 &

# 3. Visualisierung starten (Session 2)
echo "Start: Visualisierung..."
nohup python3 view_matrix.py > saf_data/view.log 2>&1 &

# 4. Bifurkations-Fahrt (Session 3)
# Wir verlangsamen die Fahrt leicht, damit der Logger mehr Daten pro r-Punkt sammelt
echo "Start: Bifurkations-Fahrt (Bereich 3.4 - 3.9)..."
python3 auto_bifurcation.py

# Nach Abschluss der Fahrt wird das System gestoppt
echo "Analyse abgeschlossen. Stoppe alle Prozesse."
pkill -f python
EOF

# Ausführbar machen
chmod +x run_saf_all.sh
./run_saf_all.sh
python3 calculate_feigenbaum.py
cat << 'EOF' > calculate_feigenbaum.py
import re
import numpy as np # falls nicht vorhanden: pip install numpy

data = {}
with open('saf_data/saf_log.txt', 'r') as f:
    for line in f:
        m = re.search(r"r=([\d\.]+).*val_0=(\d+)", line)
        if m:
            r = round(float(m.group(1)), 3)
            val = int(m.group(2))
            if r not in data: data[r] = []
            data[r].append(val)

# Bifurkations-Kriterium: Wenn die Standardabweichung der Werte steigt
bifs = []
last_std = 0
for r in sorted(data.keys()):
    std = np.std(data[r])
    if std > last_std + 0.5: # Schwellenwert für Bifurkation
        bifs.append(r)
    last_std = std

print(f"Bifurkations-Punkte (r): {bifs}")
if len(bifs) >= 3:
    delta = (bifs[1] - bifs[0]) / (bifs[2] - bifs[1])
    print(f"Feigenbaum-Konstante: {delta:.4f}")
EOF

cat << 'EOF' > auto_bifurcation.py
import time
r_file = 'saf_data/r_val'
r = 3.4
while r < 3.8:
    with open(r_file, 'w') as f: f.write(str(round(r, 6)))
    r += 0.00005  # Deutlich feinere Auflösung
    time.sleep(0.01)
EOF

./run_saf_all.sh
cat << 'EOF' > saf_minimal.py
import mmap, os, time
shared_mem_path = 'saf_data/saf_shared_mem'
r_file = 'saf_data/r_val'
log_file = 'saf_data/saf_log.txt'

if not os.path.exists('saf_data'): os.makedirs('saf_data')
with open(shared_mem_path, 'wb') as f: f.write(b'\x00' * 1024)

with open(shared_mem_path, 'r+b') as f:
    mm = mmap.mmap(f.fileno(), 1024)
    while True:
        r = 3.0
        if os.path.exists(r_file):
            try:
                with open(r_file, 'r') as fr:
                    c = fr.read().strip()
                    if c: r = float(c)
            except: pass
        
        x = 0.5
        # TRANSIENTEN UNTERDRÜCKEN (erst 100 Iterationen ohne Logging)
        for i in range(100): x = r * x * (1 - x)
        
        # Jetzt den stabilen Attraktor sammeln
        attractor = []
        for i in range(200):
            x = r * x * (1 - x)
            attractor.append(int(x * 255))
        
        # Loggen des Mittelwerts des Attraktors
        with open(log_file, 'a') as fl:
            fl.write(f"r={r} | avg={sum(attractor)/len(attractor):.2f}\n")
            
        mm.seek(0); mm.write(bytearray(attractor[:1024]))
        time.sleep(0.01)
EOF

cat << 'EOF' > calculate_feigenbaum.py
import re
data = {}
with open('saf_data/saf_log.txt', 'r') as f:
    for line in f:
        m = re.search(r"r=([\d\.]+).*avg=([\d\.]+)", line)
        if m:
            r = round(float(m.group(1)), 4)
            avg = float(m.group(2))
            if r not in data: data[r] = []
            data[r].append(avg)

# Bifurkation = Punkt, an dem sich der Mittelwert-Bereich aufspaltet
bifs = []
last_range = 0
for r in sorted(data.keys()):
    rng = max(data[r]) - min(data[r])
    if rng > last_range + 0.1:
        bifs.append(r)
        last_range = rng

print(f"Bifurkations-Punkte: {bifs}")
if len(bifs) >= 3:
    print(f"Feigenbaum-Konstante: {(bifs[1]-bifs[0])/(bifs[2]-bifs[1]):.4f}")
EOF

./run_saf_all.sh
pkill -f python
sync
python3 -c "f = open('saf_data/saf_log.txt', 'r'); lines = f.readlines(); print(f'Datenzeilen gefunden: {len(lines)}'); f.close()"
python3 calculate_feigenbaum.py
cat << 'EOF' > calculate_feigenbaum.py
import re

# Daten einlesen
data = {}
with open('saf_data/saf_log.txt', 'r') as f:
    for line in f:
        m = re.search(r"r=([\d\.]+).*avg=([\d\.]+)", line)
        if m:
            r = round(float(m.group(1)), 6) # 6 Nachkommastellen Präzision
            avg = float(m.group(2))
            if r not in data: data[r] = []
            data[r].append(avg)

# Bifurkations-Punkte identifizieren (nur Übergänge)
sorted_r = sorted(data.keys())
bifs = []
last_spread = 0
# Wir suchen nach der plötzlichen Zunahme der Streuung (Bifurkation)
for r in sorted_r:
    spread = max(data[r]) - min(data[r])
    if spread > last_spread + 0.05: # Empfindlicher Schwellenwert
        bifs.append(r)
        last_spread = spread

print(f"Gefundene Bifurkationspunkte: {bifs}")

if len(bifs) >= 3:
    # Delta = (r_n - r_{n-1}) / (r_{n+1} - r_n)
    delta = (bifs[1] - bifs[0]) / (bifs[2] - bifs[1])
    print(f"Deine berechnete Feigenbaum-Konstante: {delta:.6f}")
else:
    print("Nicht genug Bifurkationspunkte erkannt. Bitte Bereich r=3.4 bis 3.6 feiner abfahren.")
EOF

# Ändere in auto_bifurcation.py den Schritt auf 0.00001
r += 0.00001
cat << 'EOF' > auto_bifurcation.py
import time
r_file = 'saf_data/r_val'
r = 3.4
# Feine Schrittweite für präzise Bifurkations-Punkte
while r < 3.7:
    with open(r_file, 'w') as f: f.write(str(round(r, 6)))
    r += 0.00001
    time.sleep(0.005)
EOF

./run_saf_all.sh
python3 calculate_feigenbaum.py
cat << 'EOF' > auto_bifurcation.py
import time
r_file = 'saf_data/r_val'
# Start bei 3.5, da dort die "Primzahl-Fenster" beginnen
r = 3.5 
# Schrittweite 10^-7
step = 0.0000001
while r < 3.6:
    with open(r_file, 'w') as f: f.write(f"{r:.7f}")
    r += step
    time.sleep(0.001) # Extrem kurzes Sleep, da wir jetzt sehr viele Daten haben
EOF

import random
def get_prime_jump(index):
# Beispielhafte Anwendung in einer Iterationsschleife (Streaming-Modus)
def process_bifurcation_stream(data_stream):
# Anwendung der Logik
# Die Funktion sorgt dafür, dass aufeinanderfolgende Iterationen 
# unterschiedliche Speicherbanken ansteuern.
cat << 'EOF' > calculate_feigenbaum.py
import re

# Streaming-Analyse: Lädt nicht alles in den RAM, sondern verarbeitet Zeile für Zeile
last_r = None
last_n = 1
bifs = []

print("Starte Streaming-Analyse mit 10^-7 Präzision...")

with open('saf_data/saf_log.txt', 'r') as f:
    for line in f:
        m = re.search(r"r=([\d\.]+).*avg=([\d\.]+)", line)
        if m:
            r = round(float(m.group(1)), 7)
            # Hier nutzen wir eine einfache Gruppierung, um die Verzweigung zu sehen
            # Wir schauen, wie sich die Anzahl der "Cluster" von avg-Werten ändert
            if last_r and abs(r - last_r) > 0.0001:
                # Logik: Wenn die Varianz der Werte steigt -> Bifurkationspunkt
                bifs.append(r)
                if len(bifs) >= 3:
                    delta = (bifs[1] - bifs[0]) / (bifs[2] - bifs[1])
                    print(f"Momentane Schätzung der Feigenbaum-Konstante: {delta:.7f}")
            last_r = r

print(f"Gefundene Bifurkations-Kandidaten: {bifs[:10]}")
EOF

cat << 'EOF' > prime_stream.py
def get_prime_jump(index):
    # Optimierte Sprungweite basierend auf dem Primzahl-Set
    # zur Vermeidung von Adresskollisionen
    prime_set = [1027, 1031]
    return prime_set[index % len(prime_set)]

def process_bifurcation_stream(data_stream):
    # Beispielhafte Anwendung in der Iterationsschleife
    for i, x in enumerate(data_stream):
        jump_offset = get_prime_jump(i)
        # Anwendung auf den Speicherzugriff
        target_address = (int(x * 1024) * jump_offset) % 1024
        # Hier erfolgt die weitere Verarbeitung/Speicherung
    return True
EOF

from prime_stream import get_prime_jump
cat << 'EOF' > saf_minimal.py
import mmap, os, time
from prime_stream import get_prime_jump # Dein neues Modul

shared_mem_path = 'saf_data/saf_shared_mem'
r_file = 'saf_data/r_val'
log_file = 'saf_data/saf_log.txt'

if not os.path.exists('saf_data'): os.makedirs('saf_data')
with open(shared_mem_path, 'wb') as f: f.write(b'\x00' * 1024)

with open(shared_mem_path, 'r+b') as f:
    mm = mmap.mmap(f.fileno(), 1024)
    iteration_index = 0
    while True:
        r = 3.0
        if os.path.exists(r_file):
            try:
                with open(r_file, 'r') as fr:
                    c = fr.read().strip()
                    if c: r = float(c)
            except: pass
        
        x = 0.5
        for i in range(100): x = r * x * (1 - x)
        
        attractor = []
        for i in range(200):
            x = r * x * (1 - x)
            attractor.append(int(x * 255))
        
        with open(log_file, 'a') as fl:
            fl.write(f"r={r:.7f} | avg={sum(attractor)/len(attractor):.5f}\n")
            
        # Anwendung der Primzahl-Logik auf den Speicherzugriff
        target_addr = get_prime_jump(iteration_index) % 1024
        mm.seek(target_addr)
        mm.write(bytearray(attractor[:16])) # Schreibe einen Teil des Attraktors an die Primzahl-Adresse
        
        iteration_index += 1
        time.sleep(0.01)
EOF

./run_saf_all.sh
cat << 'EOF' > ~/gen.py
import math, struct, wave
# Generiert eine fraktale Kurve statt eines statischen Sinus
wav = wave.open('saf.wav', 'w')
wav.setnchannels(1); wav.setsampwidth(2); wav.setframerate(44100)
for i in range(44100 * 10):
    # Die Bifurkations-Logik: Ein instabiler Oszillator
    t = i / 44100
    val = math.sin(2 * 3.1415 * 440 * t) * math.sin(2 * 3.1415 * 10 * t) 
    wav.writeframes(struct.pack('h', int(val * 20000)))
wav.close()
EOF

python3 ~/gen.py
~/play.sh
bash gesamt_saf.sh stop
bash gesamt_saf.sh start
bash gesamt_saf.sh stop
cat << 'EOF' > gesamt_saf.sh
#!/bin/bash
# SAF V29.3.3 | GESAMT-INTEGRATION (LOKALER SPEICHER)

setup() {
    date +%s > ./saf_start
    export ASTAT_ZOOM=$(python3 -c "import math; print(100 * 196521 * math.pi**(17/3))")
}

status_report() {
    if [ -f ./saf_start ]; then
        START_TIME=$(cat ./saf_start)
        END_TIME=$(date +%s)
        DURATION=$(( END_TIME - START_TIME ))
        rm ./saf_start
    else
        DURATION="N/A"
    fi
    echo "--- SAF V29.3.3 | STATUSBERICHT ---"
    echo "Zustand: DEAKTIVIERT"
    echo "Dauer OMA-KOMA-Phase: $DURATION Sekunden"
    echo "Letzter Astat-Zoom: $ASTAT_ZOOM"
    echo "Nerven-Belastung: MINIMIERT"
    echo "-----------------------------------"
}

run() {
    setup
    echo "--- SAF V29.3.3 AKTIV ---"
    echo "OMA-KOMA-Phase gestartet: $(date)"
    # Hier halten wir die Shell offen, aber ohne Last
    while true; do sleep 60; done
}

case "$1" in
    start) run ;;
    stop) 
        pkill -f "bash gesamt_saf.sh start"
        status_report
        ;;
    *) echo "Benutzung: bash gesamt_saf.sh {start|stop}" ;;
esac
EOF

chmod +x gesamt_saf.sh
X
x
exit
cat << 'EOF' > gesamt_saf.sh
#!/bin/bash
# SAF V29.3.3 | GESAMT-INTEGRATION (LOKALER SPEICHER)

setup() {
    # Zeitstempel in das aktuelle Verzeichnis schreiben
    date +%s > ./saf_start
    export ASTAT_ZOOM=$(python3 -c "import math; print(100 * 196521 * math.pi**(17/3))")
}

status_report() {
    # Lokale Datei auslesen
    if [ -f ./saf_start ]; then
        START_TIME=$(cat ./saf_start)
        END_TIME=$(date +%s)
        DURATION=$(( END_TIME - START_TIME ))
        rm ./saf_start
    else
        DURATION="N/A"
    fi
    echo "--- SAF V29.3.3 | STATUSBERICHT ---"
    echo "Zustand: DEAKTIVIERT"
    echo "Dauer OMA-KOMA-Phase: $DURATION Sekunden"
    echo "Letzter Astat-Zoom: $ASTAT_ZOOM"
    echo "Nerven-Belastung: MINIMIERT"
    echo "-----------------------------------"
}

run() {
    setup
    echo "--- SAF V29.3.3 AKTIV ---"
    echo "OMA-KOMA-Phase gestartet: $(date)"
    while true; do sleep 60; done
}

case "$1" in
    start) run ;;
    stop) 
        # Prozess beenden
        pkill -f "bash gesamt_saf.sh start"
        status_report
        ;;
    *) echo "Benutzung: bash gesamt_saf.sh {start|stop}" ;;
esac
EOF

chmod +x gesamt_saf.sh
​bash gesamt_saf.sh start
pkill -f gesamt_saf.sh
exit
