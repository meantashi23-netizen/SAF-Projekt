import re
log_file = 'saf_data/saf_log.txt'
try:
    with open(log_file, 'r') as f:
        seen = {}
        for line in f:
            m = re.search(r"r=([\d\.]+).*val_0=(\d+)", line)
            if m:
                r, val = float(m.group(1)), int(m.group(2))
                if r not in seen: seen[r] = set()
                seen[r].add(val)
        for r in sorted(seen.keys()):
            if len(seen[r]) > 1: print(f"Bifurkation bei r={r:.4f} | Zustände: {seen[r]}")
except: print("Keine Log-Daten gefunden.")
