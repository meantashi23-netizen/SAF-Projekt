import re
# Sammle alle Punkte und berechne das Delta über die Spanne
bifs = []
with open('saf_data/saf_log.txt', 'r') as f:
    for line in f:
        m = re.search(r"r=([\d\.]+)", line)
        if m:
            bifs.append(float(m.group(1)))

# Wir nehmen die letzten Punkte, da sie am kritischen Punkt liegen
if len(bifs) >= 5:
    # Die "Feigenbaum-Skalierung": delta = (r_{n} - r_{n-1}) / (r_{n+1} - r_{n})
    # Wir nehmen die letzten drei Abstände
    d1 = bifs[-2] - bifs[-3]
    d2 = bifs[-1] - bifs[-2]
    # Das Verhältnis zeigt die Stauchung
    delta = d1 / d2 if d2 != 0 else 0
    print(f"DNA-Ende: {bifs[-5:]}")
    print(f"Aktuelles Delta: {delta:.4f}")
