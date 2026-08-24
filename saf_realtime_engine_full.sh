#!/bin/bash
# SAF Multiband Visualizer Engine (Desktop Auto-Search Edition)

# Pfad-Prüfung: Prüfe zuerst Home-Ordner, dann Desktop
AUDIO_NAME="Recording_2026-07-30_01h50m56s.wav"

if [ -f "$AUDIO_NAME" ]; then
    AUDIO_INPUT="$AUDIO_NAME"
elif [ -f "$HOME/Desktop/$AUDIO_NAME" ]; then
    AUDIO_INPUT="$HOME/Desktop/$AUDIO_NAME"
else
    # Falls der Name leicht abweicht, nimm die neuste .wav vom Desktop
    AUDIO_INPUT=$(ls -t ~/Desktop/*.wav 2>/dev/null | head -n 1)
fi

BACKGROUND_IMG="saf_v29_visual.jpg"
OUTPUT_STREAM="saf_realtime_matrix_full.mp4"

if [ -z "$AUDIO_INPUT" ] || [ ! -f "$AUDIO_INPUT" ]; then
    echo "Fehler: Keine passende .wav Datei auf dem Desktop gefunden!"
    exit 1
fi

echo "=== Gefundene Audio-Quelle: $AUDIO_INPUT ==="
echo "=== Starte SAF Multi-Band Processing ==="

# Erstelle Platzhalter-Hintergrundbild falls nicht vorhanden
if [ ! -f "$BACKGROUND_IMG" ] && [ ! -f "$HOME/Desktop/$BACKGROUND_IMG" ]; then
    echo "Erstelle Platzhalter-Hintergrundbild..."
    ffmpeg -y -f lavfi -i color=c=0x040914:s=1920x1080 -vframes 1 "$BACKGROUND_IMG" >/dev/null 2>&1
elif [ -f "$HOME/Desktop/$BACKGROUND_IMG" ]; then
    BACKGROUND_IMG="$HOME/Desktop/$BACKGROUND_IMG"
fi

# Multi-Band Spektral-Rendering
ffmpeg -y -i "$AUDIO_INPUT" -loop 1 -i "$BACKGROUND_IMG" \
  -filter_complex "
    [1:v]scale=1920:1080[bg];
    
    [0:a]lowpass=f=120,showwaves=s=1600x120:mode=cline:colors=0xff0055@0.9[b1];
    [0:a]bandpass=f=260:width_type=h:w=280,showwaves=s=1600x120:mode=cline:colors=0xffaa00@0.85[b2];
    [0:a]bandpass=f=950:width_type=h:w=1100,showwaves=s=1600x120:mode=cline:colors=0x00ff66@0.85[b3];
    [0:a]bandpass=f=3250:width_type=h:w=3500,showwaves=s=1600x120:mode=cline:colors=0x00ffff@0.85[b4];
    [0:a]highpass=f=5000,showwaves=s=1600x120:mode=cline:colors=0xaa00ff@0.9[b5];

    [bg][b1]overlay=160:180:shortest=1[v1];
    [v1][b2]overlay=160:320:shortest=1[v2];
    [v2][b3]overlay=160:460:shortest=1[v3];
    [v3][b4]overlay=160:600:shortest=1[v4];
    [v4][b5]overlay=160:740:shortest=1[out]
  " \
  -map "[out]" -map 0:a -c:v libx264 -preset fast -crf 18 -c:a aac -b:a 320k "$OUTPUT_STREAM"

echo "=== Processing erfolgreich beendet: $OUTPUT_STREAM ==="
