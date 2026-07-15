import mmap, os, time
# Keine externen Importe für diesen Test, um Fehlerquellen zu minimieren
shared_mem_path = 'saf_data/saf_shared_mem'
r_file = 'saf_data/r_val'
log_file = 'saf_data/saf_log.txt'

with open(shared_mem_path, 'wb') as f: f.write(b'\x00' * 1024)

while True:
    r = 3.5 # Sicherer Startwert
    if os.path.exists(r_file):
        try:
            with open(r_file, 'r') as fr:
                content = fr.read().strip()
                if content: r = float(content)
        except: pass
    
    # Vereinfachte logistische Iteration
    x = 0.5
    for i in range(50): x = r * x * (1 - x)
    
    # Schreiben mit Line-Buffering
    with open(log_file, 'a', buffering=1) as fl:
        fl.write(f"r={r:.7f} | val={x:.5f}\n")
        
    time.sleep(0.1) # Drosselung auf 100ms für maximale Stabilität
