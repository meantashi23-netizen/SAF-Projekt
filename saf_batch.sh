#!/bin/bash

# --- KONFIGURATION ---
INPUT_DIR="./lidar_raw_data"
OUTPUT_DIR="./exports"
# Ziel: Dein Android-Download-Ordner (unterteilt in einen sauberen Unterordner)
DOWNLOAD_DIR="$HOME/storage/shared/Download/saf_output"

# Stelle sicher, dass die Ordner existieren
mkdir -p "$OUTPUT_DIR"
mkdir -p "$DOWNLOAD_DIR"

echo "=== SAF BATCH-PROZESS GESTARTET ==="

# Loop über alle PCD-Dateien
for file in "$INPUT_DIR"/*.pcd; do
    [ -e "$file" ] || continue # Falls keine Dateien vorhanden sind
    filename=$(basename "$file")
    
    echo "Verarbeite: $filename..."
    # Hier wird dein Python-Skript aufgerufen
    python3 saf_mobile_infer.py --input "$file" --output "$OUTPUT_DIR/$filename"
done

# Transfer zum Android-Viewer
echo "=== KOPIERE DATEIEN ZUM ANDROID-DOWNLOAD-ORDNER ==="
cp "$OUTPUT_DIR"/*.pcd "$DOWNLOAD_DIR/"

echo "----------------------------------------------------"
echo "FERTIG!"
echo "Deine gefilterten Punktwolken liegen bereit unter:"
echo "Download/saf_output/ in deiner Viewer-App."
echo "----------------------------------------------------"
#!/bin/bash
# SAF V29.3.3 Batch-Prozessor

INPUT_DIR="lidar_raw_data"
OUTPUT_DIR="exports"

# Verzeichnisse sicherstellen
mkdir -p "$OUTPUT_DIR"

echo "Starte Batch-Verarbeitung..."

for file in "$INPUT_DIR"/*.pcd; do
    if [ -e "$file" ]; then
        filename=$(basename "$file")
        echo "Verarbeite: $filename"

        # Hier rufen wir dein Skript auf
        # Hinweis: Du musst sicherstellen, dass dein Skript den Input-Pfad akzeptiert
        python3 saf_mobile_infer.py "$file" "$OUTPUT_DIR/$filename"

        echo "Fertig: $OUTPUT_DIR/$filename"
    fi
done

echo "Alle Dateien verarbeitet."
