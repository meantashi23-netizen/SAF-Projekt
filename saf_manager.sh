import numpy as np
import os

def load_pcd(filepath):
    """
    Liest .pcd Dateien (ASCII). 
    Sucht nach der Zeile 'DATA ascii' und liest alles danach.
    """
    with open(filepath, 'r') as f:
        # Finde die Zeile, wo die Daten anfangen
        lines = f.readlines()
        data_start_idx = 0
        for i, line in enumerate(lines):
            if "DATA ascii" in line:
                data_start_idx = i + 1
                break
        
        # Konvertiere den Rest zu einem numpy array
        data = np.loadtxt(lines[data_start_idx:])
        return data[:, :3] # Extrahiere nur X, Y, Z

def save_pcd(filepath, points):
    """
    Schreibt Punktwolken im korrekten .pcd Format.
    Dies ist essenziell für die Kompatibilität mit externer Software.
    """
    num_points = len(points)
    header = [
        "VERSION .7",
        "FIELDS x y z",
        "SIZE 4 4 4",
        "TYPE F F F",
        "COUNT 1 1 1",
        f"WIDTH {num_points}",
        "HEIGHT 1",
        "VIEWPOINT 0 0 0 1 0 0 0",
        f"POINTS {num_points}",
        "DATA ascii"
    ]
    
    with open(filepath, 'w') as f:
        f.write("\n".join(header) + "\n")
        np.savetxt(f, points, fmt="%.6f") # Schreibt die Koordinaten
def save_config(threshold):
    with open("config.saf", "w") as f:
        f.write(str(threshold))

def load_config():
    if os.path.exists("config.saf"):
        with open("config.saf", "r") as f:
            return float(f.read())
    return 0.15 # Fallback-Wert

# Im main-Block:
# Statt threshold hart zu codieren, laden wir ihn:
start_threshold = load_config()

# Wenn du das nächste Mal den adaptiven Filter aufrufst:
processed_pcd, used_threshold = adaptive_filter(raw_pcd, target_count=target)

# Nach der Optimierung speichern wir den neuen Bestwert:
save_config(used_threshold)

def adaptive_filter(points, target_count=200):
    """
    Passt den Schwellenwert automatisch an, um die Zielanzahl an Punkten zu erreichen.
    """
    threshold = 0.15 # Startwert
    best_points = np.array([])
    
    # Wir erlauben maximal 10 Iterationen, um das System nicht zu überlasten
    for i in range(10):
        # Filterung anwenden
        current_points, _ = fractal_valency_filter(points, threshold)
        count = len(current_points)
        
        # Prüfung: Sind wir nah genug an der Zielzahl?
        # Toleranzbereich: 10% Abweichung
        if abs(count - target_count) < (target_count * 0.1):
            return current_points, threshold
        
        # Anpassung des Schwellenwerts
        if count < target_count:
            threshold += 0.05 # Filter öffnen (mehr Punkte)
        else:
            threshold -= 0.02 # Filter schließen (weniger Punkte)
            
        # Sicherheitsabbruch, wenn Threshold negativ wird
        if threshold <= 0.01:
            threshold = 0.01
            break
            
    return current_points, threshold
def adaptive_filter(points, target_count=200):
    threshold = 0.2
    for i in range(5): # Iteratives Annähern an die Zielmenge
        processed, _ = fractal_valency_filter(points, threshold)
        count = len(processed)
        if count < target_count:
            threshold += 0.05 # Filter öffnen
        elif count > target_count:
            threshold -= 0.05 # Filter schließen
    return processed
def analyze_cloud(points, distances):
    """Führt eine statische Analyse der Punktwolke durch."""
    if len(points) == 0:
        return "Keine Punkte zur Analyse vorhanden."
    
    # Berechnungen
    mean_dist = np.mean(np.abs(distances)) # Wie nah sind wir am perfekten Fraktal-Rand?
    std_dist = np.std(np.abs(distances))   # Wie stark schwanken die Punkte?
    bounding_box = [np.min(points, axis=0), np.max(points, axis=0)]
    
    report = f"""
--- STATISTISCHE ANALYSE ---
Anzahl Punkte: {len(points)}
Mittlere Abweichung (SDF): {mean_dist:.4f}
Streuung (StdDev): {std_dist:.4f}
Ausdehnung (Min/Max): 
   Min: {bounding_box[0]}
   Max: {bounding_box[1]}
---------------------------
"""
    return report
def mandelbox_sdf(p):
    # Parametrierung für das Tuning
    scale = 2.5    # <-- Erhöhe diesen Wert (z.B. auf 3.0), um die Geometrie zu "zerren"
    iterations = 6 # <-- Erhöhe diesen Wert, um feinere fraktale Details zu erhalten
    
    for _ in range(iterations):
        p = np.clip(p, -1, 1) * 2.0 - p
        r2 = np.sum(p**2)
        if r2 < 0.5:
            p *= scale
        elif r2 < 1.0:
            p /= r2
    return np.linalg.norm(p) - 0.5
#!/bin/bash
# SAF V29.3.3 Master-Manager
# 1. Deployment sichern
# 2. Python-Modul editieren
# 3. Pipeline starten

echo "SAF V29.3.3 System aktiv."
echo "Wähle eine Aktion:"
echo "1) Inferenz-Modul editieren (nano)"
echo "2) Pipeline ausführen (Start)"
echo "3) Exit"
read -p "Deine Wahl: " choice

case $choice in
    1)
        nano saf_mobile_infer.py
        ;;
    2)
        echo "Starte SAF-Pipeline..."
        python3 saf_mobile_infer.py
        ;;
    3)
        exit
        ;;
    *)
        echo "Ungültige Wahl."
        ;;
esac
if __name__ == "__main__":
    # ... (vorheriger Code zum Laden/Generieren)
    
    # Filterung
    processed_pcd, scores = fractal_valency_filter(raw_pcd)
    
    # STATISTISCHE ANALYSE AUFRUFEN
    stats = analyze_cloud(processed_pcd, scores)
    print(stats)
    
    # Export...
def adaptive_filter(points, target_count=200):
    """
    Passt den Schwellenwert automatisch an, um die Zielanzahl an Punkten zu erreichen.
    """
    threshold = 0.15 # Startwert
    best_points = np.array([])
    
    # Wir erlauben maximal 10 Iterationen, um das System nicht zu überlasten
    for i in range(10):
        # Filterung anwenden
        current_points, _ = fractal_valency_filter(points, threshold)
        count = len(current_points)
        
        # Prüfung: Sind wir nah genug an der Zielzahl?
        # Toleranzbereich: 10% Abweichung
        if abs(count - target_count) < (target_count * 0.1):
            return current_points, threshold
        
        # Anpassung des Schwellenwerts
        if count < target_count:
            threshold += 0.05 # Filter öffnen (mehr Punkte)
        else:
            threshold -= 0.02 # Filter schließen (weniger Punkte)
            
        # Sicherheitsabbruch, wenn Threshold negativ wird
        if threshold <= 0.01:
            threshold = 0.01
            break
            
    return current_points, threshold
if __name__ == "__main__":
    input_file = "lidar_raw_data/input.pcd"
    output_file = "lidar_raw_data/filtered_output.pcd"
    
    # 1. Laden
    if os.path.exists(input_file):
        raw_pcd = load_pcd(input_file)
        print(f"Lade {len(raw_pcd)} Punkte aus {input_file}")
    else:
        print("Keine Eingabedatei gefunden, generiere Simulationsdaten.")
        raw_pcd = np.random.uniform(-1.5, 1.5, (2000, 3))
    
    # 2. Adaptive Filterung (wie zuvor etabliert)
    processed_pcd, threshold = adaptive_filter(raw_pcd, target_count=250)
    
    # 3. Export
    if len(processed_pcd) > 0:
        save_pcd(output_file, processed_pcd)
        print(f"Export erfolgreich nach {output_file} ({len(processed_pcd)} Punkte)")
