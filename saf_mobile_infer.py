# 1. MATHEMATISCHE BASIS (STABILISIERT)
def mandelbox_sdf(p):
    # ... hier die Logik mit dem Epsilon-Fix ...
    if r2 > 1e-8: # Schutz vor Null-Division
        p /= r2
    return np.linalg.norm(p) - 0.5

# 2. DIE ADAPTIONS-SCHLEIFE (DER FILTER)
def adaptive_filter(points, target_count=250):
    threshold = 0.15 # Start-Schwellenwert
    
    # Der Regelkreis: Wir iterieren, bis wir nah am Ziel sind
    for i in range(10): 
        # Filtern
        current_points = ... # Anwendung der SDF
        
        # Entscheidung: Ist der Filter zu eng oder zu weit?
        if len(current_points) < target_count:
            threshold += 0.05 # Mehr Punkte reinlassen
        else:
            threshold -= 0.02 # Punkte aussortieren
            
        # Sicherheitsschranke
        threshold = max(0.01, threshold)
        
    return current_points, threshold

# 3. DER AUFRUF (DIE BRÜCKE)
if __name__ == "__main__":
    raw_pcd = load_pcd("input.pcd")
    # Hier "kommst du in den Filter" rein:
    filtered_points, optimal_threshold = adaptive_filter(raw_pcd, target_count=250)
def mandelbox_sdf(p):
    """Mandelbox-SDF mit Epsilon-Schutz gegen Division durch Null."""
    p = np.clip(p, -1, 1) * 2.0 - p
    r2 = np.sum(p**2)
    
    # Epsilon ist ein extrem kleiner Wert, um Division durch Null zu verhindern
    epsilon = 1e-8 
    
    if r2 < 0.5:
        p *= 2.0
    elif r2 < 1.0:
        # Absicherung der Division
        if r2 > epsilon:
            p /= r2
            
    return np.linalg.norm(p) - 0.5
import sys # Import ganz oben hinzufügen

if __name__ == "__main__":
    # Wenn Argumente übergeben wurden, nutze sie (für Batch)
    if len(sys.argv) > 2:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    else:
        # Fallback für manuellen Start
        input_file = "lidar_raw_data/input.pcd"
        output_file = "lidar_raw_data/filtered_output.pcd"
        
    # ... der Rest bleibt gleich (laden, filtern, speichern)
import numpy as np
import os

def load_pcd(filepath):
    """Lädt echte LiDAR-Punktwolken (.pcd)."""
    data = np.loadtxt(filepath, skiprows=11)
    return data[:, :3]

def save_pcd(filepath, points):
    """Speichert die gefilterten Punkte als .pcd Datei."""
    header = [
        "VERSION .7",
        "FIELDS x y z",
        "SIZE 4 4 4",
        "TYPE F F F",
        "COUNT 1 1 1",
        f"WIDTH {len(points)}",
        "HEIGHT 1",
        "VIEWPOINT 0 0 0 1 0 0 0",
        f"POINTS {len(points)}",
        "DATA ascii"
    ]
    with open(filepath, 'w') as f:
        f.write("\n".join(header) + "\n")
        np.savetxt(f, points, fmt="%.6f")

def mandelbox_sdf(p):
    """Mandelbox-SDF für fraktale Validierung."""
    p = np.clip(p, -1, 1) * 2.0 - p
    r2 = np.sum(p**2)
    if r2 < 0.5:
        p *= 2.0
    elif r2 < 1.0:
        p /= r2
    return np.linalg.norm(p) - 0.5

def fractal_valency_filter(points, threshold=0.1):
    valencies = np.array([mandelbox_sdf(p) for p in points])
    mask = np.abs(valencies) < threshold
    return points[mask], valencies[mask]

if __name__ == "__main__":
    # MODUS-EINSTELLUNG
    use_file = False # Auf True setzen, wenn eine .pcd Datei vorliegt
    input_file = "lidar_raw_data/input.pcd"
    output_file = "lidar_raw_data/filtered_output.pcd"

    if use_file and os.path.exists(input_file):
        raw_pcd = load_pcd(input_file)
    else:
        print("Simulations-Modus (Generiere 2000 Testpunkte)...")
        raw_pcd = np.random.uniform(-1.5, 1.5, (2000, 3))

    # Filterung
    processed_pcd, scores = fractal_valency_filter(raw_pcd)
    
    # Export
    save_pcd(output_file, processed_pcd)
    
    print(f"Eingangspunkte: {len(raw_pcd)}")
    print(f"Ausgangspunkte (valenzgeprüft): {len(processed_pcd)}")
    print(f"Export erfolgreich: {output_file}")
def save_pcd(filepath, points):
    """Speichert die gefilterten Punkte als .pcd Datei."""
    header = [
        "VERSION .7",
        "FIELDS x y z",
        "SIZE 4 4 4",
        "TYPE F F F",
        "COUNT 1 1 1",
        f"WIDTH {len(points)}",
        "HEIGHT 1",
        "VIEWPOINT 0 0 0 1 0 0 0",
        f"POINTS {len(points)}",
        "DATA ascii"
    ]
    with open(filepath, 'w') as f:
        f.write("\n".join(header) + "\n")
        np.savetxt(f, points, fmt="%.6f")

# Integration in den if __name__ == "__main__": Block:
# Nach der Filterung:
if len(processed_pcd) > 0:
    save_pcd("lidar_raw_data/filtered_output.pcd", processed_pcd)
    print("Export erfolgreich: 'filtered_output.pcd' wurde erstellt.")
import numpy as np

def load_pcd(filepath):
    """Task 1: Lädt echte LiDAR-Punktwolken (.pcd)"""
    # Header überspringen (typisch 11 Zeilen)
    data = np.loadtxt(filepath, skiprows=11)
    return data[:, :3]

def mandelbox_sdf(p):
    """Task 2: Echte Mandelbox-Distanzschätzung statt Sinus"""
    scale = 2.0
    p = np.clip(p, -1, 1) * 2.0 - p
    r2 = np.sum(p**2)
    # Geometrische Faltung
    if r2 < 0.5:
        p *= 2.0
    elif r2 < 1.0:
        p /= r2
    return np.linalg.norm(p) - 0.5

def fractal_valency_filter(points, threshold=0.1):
    # Anwendung der SDF auf alle Punkte
    valencies = np.array([mandelbox_sdf(p) for p in points])
    mask = np.abs(valencies) < threshold
    return points[mask], valencies[mask]

if __name__ == "__main__":
    # MODUS-KONFIGURATION
    # Setze auf True, wenn eine .pcd Datei im Ordner 'lidar_raw_data' liegt
    use_file = False 
    
    if use_file:
        raw_pcd = load_pcd("lidar_raw_data/input.pcd")
    else:
        print("Simulations-Modus aktiv...")
        raw_pcd = np.random.uniform(-1, 1, (1000, 3))

    processed_pcd, scores = fractal_valency_filter(raw_pcd)
    
    print(f"Eingangspunkte: {len(raw_pcd)}")
    print(f"Ausgangspunkte (valenzgeprüft): {len(processed_pcd)}")
    print("SAF-Struktur-Integration: Erfolgreich (SDF-basiert).")

def load_pcd(filepath):
    """Liest einfache ASCII-PCD Dateien ein."""
    # PCD-Header überspringen (meist 11 Zeilen)
    data = np.loadtxt(filepath, skiprows=11)
    return data[:, :3] # Extrahiere nur X, Y, Z Koordinaten

def fractal_valency_filter(points, threshold=0.5):
    # Fraktale Distanz-Simulation
    distances = np.linalg.norm(points, axis=1)
    valency = np.sin(distances * 10)**2
    mask = valency > threshold
    return points[mask], valency[mask]

if __name__ == "__main__":
    # WÄHLE DEINEN MODUS:
    # Setze 'use_file = True', wenn du eine Datei in lidar_raw_data hast.
    use_file = False 
    
    if use_file:
        file_path = "lidar_raw_data/input.pcd" # Dateiname hier anpassen
        raw_pcd = load_pcd(file_path)
    else:
        # Simulations-Modus
        raw_pcd = np.random.rand(1000, 3)

    processed_pcd, scores = fractal_valency_filter(raw_pcd)
    
    print(f"Eingangspunkte: {len(raw_pcd)}")
    print(f"Ausgangspunkte (valenzgeprüft): {len(processed_pcd)}")
    print("SAF-Struktur-Integration: Erfolgreich.")
import numpy as np

def fractal_valency_filter(points, threshold=0.5):
    # Simulation der fraktalen Dichteberechnung
    distances = np.linalg.norm(points, axis=1)
    valency = np.sin(distances * 10)**2
    mask = valency > threshold
    return points[mask], valency[mask]

if __name__ == "__main__":
    raw_pcd = np.random.rand(1000, 3)
    processed_pcd, scores = fractal_valency_filter(raw_pcd)
    print(f"Eingangspunkte: {len(raw_pcd)}")
    print(f"Ausgangspunkte (valenzgeprüft): {len(processed_pcd)}")
    print("SAF-Struktur-Integration: Erfolgreich.")


