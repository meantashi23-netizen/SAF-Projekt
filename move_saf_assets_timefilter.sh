#!/bin/bash
# SAF Time-Filtered Asset Collector (Seit gestern 22:00 Uhr)

TARGET_DIR="$HOME/Desktop/5D-SAF Set/Video & π5"

echo "=== 1. Erstelle Zielordner: $TARGET_DIR ==="
mkdir -p "$TARGET_DIR"

# Erstelle temporäre Referenz-Datei für den Zeitstempel (gestern 22:00 Uhr)
# Format: YYYYMMDDhhmm (202607292200)
REF_TIME="202607292200"
TOUCH_REF="/tmp/saf_time_ref"
touch -t "$REF_TIME" "$TOUCH_REF"

echo "=== 2. Suche Dateien ab 29. Juli 22:00 Uhr ==="

# Funktion zum Verschieben gefilterter Dateien
move_recent_files() {
    SRC_DIR="$1"
    PATTERN="$2"
    if [ -d "$SRC_DIR" ]; then
        find "$SRC_DIR" -maxdepth 1 -type f \( -name "$PATTERN" \) -newer "$TOUCH_REF" -exec mv -v {} "$TARGET_DIR/" \;
    fi
}

# 1. Alle im Terminal generierten / aktuellen WAVs und MP4s im aktuellen Ordner
find . -maxdepth 1 -type f \( -name "*.wav" -o -name "*.mp4" \) -newer "$TOUCH_REF" -exec mv -v {} "$TARGET_DIR/" \;

# 2. Relevante Dateien vom Desktop
move_recent_files "$HOME/Desktop" "*.wav"
move_recent_files "$HOME/Desktop" "*.mp4"

# 3. Traktor Recordings (nur ab gestern 22:00)
move_recent_files "$HOME/Music/Traktor/Recordings" "*.wav"
move_recent_files "$HOME/Music/Native Instruments/Traktor 4/Recordings" "*.wav"

# Aufräumen
rm -f "$TOUCH_REF"

echo "=== Verschieben abgeschlossen! Gefilterte Dateien liegen in: ==="
echo "$TARGET_DIR"
