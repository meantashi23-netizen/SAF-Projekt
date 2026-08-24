#!/bin/bash
# SAF PNG Asset Collector (Downloads -> 5D-SAF Set/Video & π5)

TARGET_DIR="$HOME/Desktop/5D-SAF Set/Video & π5"
DOWNLOADS_DIR="$HOME/Downloads"

echo "=== 1. Prüfe Zielordner: $TARGET_DIR ==="
mkdir -p "$TARGET_DIR"

echo "=== 2. Verschiebe .png Dateien aus $DOWNLOADS_DIR ==="

if [ -d "$DOWNLOADS_DIR" ]; then
    # Verschiebe alle .png Dateien aus dem Downloads-Ordner
    mv -v "$DOWNLOADS_DIR"/*.png "$TARGET_DIR/" 2>/dev/null
    mv -v "$DOWNLOADS_DIR"/*.PNG "$TARGET_DIR/" 2>/dev/null
    echo "=== PNGs erfolgreich verschoben! ==="
else
    echo "Fehler: Downloads-Ordner nicht gefunden."
fi

