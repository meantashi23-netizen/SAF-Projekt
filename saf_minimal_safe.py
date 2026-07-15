import os, time
# Einzelschuss-Kernel: Keine Endlosschleife
log_file = 'saf_data/saf_log.txt'
if not os.path.exists('saf_data'): os.makedirs('saf_data')

r = 3.57 # Kritischer Punkt
x = 0.5
with open(log_file, 'a', buffering=1) as fl:
    for i in range(1000): # Begrenzte Anzahl, um Absturz zu verhindern
        x = r * x * (1 - x)
        fl.write(f"i={i} | val={x:.7f}\n")
        if i % 100 == 0: time.sleep(0.01)
print("Berechnung beendet. System stabil.")
