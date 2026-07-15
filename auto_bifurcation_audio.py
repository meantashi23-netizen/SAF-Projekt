import time
r = 3.4
# Exponentieller Fokus auf den kritischen Bereich (wo es chaotisch wird)
step = 0.001
while r < 3.572:
    with open('saf_data/r_val', 'w') as f: f.write(f"{r:.7f}")
    step *= 0.999 # Extrem langsame Beschleunigung für hörbare Übergänge
    r += step
    time.sleep(0.01)
