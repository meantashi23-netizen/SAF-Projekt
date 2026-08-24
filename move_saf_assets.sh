#!/bin/bash
# SAF Automated Asset Collector & File Organizer

TARGET_DIR="$HOME/Desktop/5D-SAF Set/Video & π5"

echo "=== 1. Erstelle Zielordner: $TARGET_DIR ==="
mkdir -p "$TARGET_DIR"

echo "=== 2. Suche und verschiebe alle SAF MP4 & WAV Dateien ==="

# Verschiebe alle Audio/Video-Dateien aus dem aktuellen Arbeitsverzeichnis
mv -v ./*.mp4 ./*.wav "$TARGET_DIR/" 2>/dev/null

# Verschiebe Audio/Video-Dateien vom Desktop
mv -v "$HOME/Desktop"/*.mp4 "$HOME/Desktop"/*.wav "$TARGET_DIR/" 2>/dev/null

# Verschiebe Aufnahmen aus Standard Traktor-Ordnern (falls vorhanden)
TRAKTOR_DIR1="$HOME/Music/Traktor/Recordings"
TRAKTOR_DIR2="$HOME/Music/Native Instruments/Traktor 4/Recordings"

if [ -d "$TRAKTOR_DIR1" ]; then
    mv -v "$TRAKTOR_DIR1"/*.wav "$TARGET_DIR/" 2>/dev/null
fi

if [ -d "$TRAKTOR_DIR2" ]; then
    mv -v "$TRAKTOR_DIR2"/*.wav "$TARGET_DIR/" 2>/dev/null
fi

echo "=== Verschieben abgeschlossen! Alle Dateien liegen nun in: ==="
echo "$TARGET_DIR"
