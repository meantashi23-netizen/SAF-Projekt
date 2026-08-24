#!/bin/bash
# SAF MP4 Batch-Kompressor (CRF 19 - Visuell Verlustfrei)
set -e

TARGET_DIR="$HOME/Desktop/5D-SAF Set/Video & π5"
OUTPUT_DIR="$TARGET_DIR/compressed"

mkdir -p "$OUTPUT_DIR"

echo "=== SAF Batch-Kompression gestartet ==="
echo "Zielordner: $TARGET_DIR"
echo "Ausgabeordner: $OUTPUT_DIR"
echo "--------------------------------------------------"

# Durchläuft alle .mp4 Dateien im Zielordner
for file in "$TARGET_DIR"/*.mp4; do
    # Prüfen, ob Dateien existieren
    [ -e "$file" ] || continue
    
    filename=$(basename "$file")
    outpath="$OUTPUT_DIR/$filename"
    
    # Falls die Datei im compressed-Ordner schon existiert, überspringen
    if [ -f "$outpath" ]; then
        echo "[ÜBERSPRUNGEN] Bereits komprimiert: $filename"
        continue
    fi
    
    echo "Komprimiere: $filename ..."
    
    ffmpeg -y -i "$file" \
      -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p \
      -c:a aac -b:a 256k \
      "$outpath" < /dev/null
      
    echo "--> Fertig: $filename"
    echo "--------------------------------------------------"
done

echo "=== Alle Videos erfolgreich komprimiert! ==="
