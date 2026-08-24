#!/bin/bash
# SAF Traktor Restoration Script: Verschiebt Traktor-Aufnahmen zurück in ihren Ursprungsordner

SAF_DIR="$HOME/Desktop/5D-SAF Set/Video & π5"

# Mögliche Traktor Recordings Ordner
TRAKTOR_DIR1="$HOME/Music/Native Instruments/Traktor 4/Recordings"
TRAKTOR_DIR2="$HOME/Music/Traktor/Recordings"

# Bestimme den aktiven Traktor-Ordner
if [ -d "$TRAKTOR_DIR1" ]; then
    TARGET_TRAKTOR="$TRAKTOR_DIR1"
elif [ -d "$TRAKTOR_DIR2" ]; then
    TARGET_TRAKTOR="$TRAKTOR_DIR2"
else
    # Falls keiner existiert, erstelle den Traktor 4 Standard-Ordner
    TARGET_TRAKTOR="$TRAKTOR_DIR1"
    mkdir -p "$TARGET_TRAKTOR"
fi

echo "=== Traktor Zielpfad: $TARGET_TRAKTOR ==="

if [ -d "$SAF_DIR" ]; then
    # Verschiebe alle Traktor-Recordings (typischerweise 'Recording_...' oder 'Traktor_...') zurück
    echo "=== Stelle Traktor-Dateien zurück... ==="
    
    # 1. Spezifische Traktor-Dateinamensmuster zurückschieben
    find "$SAF_DIR" -maxdepth 1 -type f \( -name "Recording_*.wav" -o -name "Traktor_*.wav" \) -exec mv -v {} "$TARGET_TRAKTOR/" \;

    echo "=== Wiederherstellung abgeschlossen! Traktor kann die Dateien wieder laden. ==="
else
    echo "Fehler: Ordner $SAF_DIR nicht gefunden."
fi
