import time
r = 3.5
# Exponentieller Fokus auf den kritischen Bereich
step = 0.001
while r < 3.571:
    with open('saf_data/r_val', 'w') as f: f.write(f"{r:.7f}")
    # Schrittweite verfeinern für maximale Präzision bei 3.57
    step *= 0.99
    r += step
    time.sleep(0.01)
