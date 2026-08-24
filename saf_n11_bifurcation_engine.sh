#!/bin/bash
# SAF N=11 Spectral Band Engine (Desktop 5D-SAF Folder Edition)

# Pfad zum Zielordner
SAF_DIR="$HOME/Desktop/5D-SAF Set/Video & π5"
AUDIO_NAME="Recording_2026-07-30_01h50m56s.wav"

# 1. Suche im SAF-Projektordner
if [ -f "$SAF_DIR/$AUDIO_NAME" ]; then
    AUDIO_INPUT="$SAF_DIR/$AUDIO_NAME"
elif [ -d "$SAF_DIR" ]; then
    # Nimmt die neuste WAV aus dem SAF-Ordner
    AUDIO_INPUT=$(ls -t "$SAF_DIR"/*.wav 2>/dev/null | head -n 1)
fi

# 2. Fallbacks (Desktop / Aktueller Ordner)
if [ -z "$AUDIO_INPUT" ] || [ ! -f "$AUDIO_INPUT" ]; then
    if [ -f "$AUDIO_NAME" ]; then
        AUDIO_INPUT="$AUDIO_NAME"
    elif [ -f "$HOME/Desktop/$AUDIO_NAME" ]; then
        AUDIO_INPUT="$HOME/Desktop/$AUDIO_NAME"
    fi
fi

BACKGROUND_IMG="saf_v29_visual.jpg"
OUTPUT_STREAM="$SAF_DIR/saf_n11_bifurcation_matrix.mp4"

if [ -z "$AUDIO_INPUT" ] || [ ! -f "$AUDIO_INPUT" ]; then
    echo "Fehler: Keine .wav Audioquelle im SAF-Ordner gefunden!"
    exit 1
fi

echo "=== SAF N=11 Spektral-Processing gestartet ==="
echo "=== Audioquelle: $AUDIO_INPUT ==="

# Prüfe Hintergrundbild (Ordner oder Lokal)
if [ -f "$SAF_DIR/$BACKGROUND_IMG" ]; then
    BACKGROUND_IMG="$SAF_DIR/$BACKGROUND_IMG"
elif [ -f "$HOME/Desktop/$BACKGROUND_IMG" ]; then
    BACKGROUND_IMG="$HOME/Desktop/$BACKGROUND_IMG"
elif [ ! -f "$BACKGROUND_IMG" ]; then
    ffmpeg -y -f lavfi -i color=c=0x030712:s=1920x1080 -vframes 1 "$BACKGROUND_IMG" >/dev/null 2>&1
fi

# N=11 Spektralbänder Rendering
ffmpeg -y -i "$AUDIO_INPUT" -loop 1 -i "$BACKGROUND_IMG" \
  -filter_complex "
    [1:v]scale=1920:1080[bg];
    
    [0:a]lowpass=f=60,showwaves=s=1680x60:mode=cline:colors=0xff0033@0.9[b1];
    [0:a]bandpass=f=105:width_type=h:w=90,showwaves=s=1680x60:mode=cline:colors=0xff3300@0.85[b2];
    [0:a]bandpass=f=250:width_type=h:w=200,showwaves=s=1680x60:mode=cline:colors=0xff9900@0.85[b3];
    [0:a]bandpass=f=525:width_type=h:w=350,showwaves=s=1680x60:mode=cline:colors=0xccff00@0.85[b4];
    [0:a]bandpass=f=1050:width_type=h:w=700,showwaves=s=1680x60:mode=cline:colors=0x33ff00@0.85[b5];
    [0:a]bandpass=f=2100:width_type=h:w=1400,showwaves=s=1680x60:mode=cline:colors=0x00ff66@0.85[b6];
    [0:a]bandpass=f=3900:width_type=h:w=2200,showwaves=s=1680x60:mode=cline:colors=0x00ffff@0.85[b7];
    [0:a]bandpass=f=6500:width_type=h:w=3000,showwaves=s=1680x60:mode=cline:colors=0x0088ff@0.85[b8];
    [0:a]bandpass=f=10000:width_type=h:w=4000,showwaves=s=1680x60:mode=cline:colors=0x3300ff@0.85[b9];
    [0:a]bandpass=f=14000:width_type=h:w=4000,showwaves=s=1680x60:mode=cline:colors=0x9900ff@0.85[b10];
    [0:a]highpass=f=16000,showwaves=s=1680x60:mode=cline:colors=0xff00cc@0.9[b11];

    [bg][b1]overlay=120:90:shortest=1[v1];
    [v1][b2]overlay=120:165:shortest=1[v2];
    [v2][b3]overlay=120:240:shortest=1[v3];
    [v3][b4]overlay=120:315:shortest=1[v4];
    [v4][b5]overlay=120:390:shortest=1[v5];
    [v5][b6]overlay=120:465:shortest=1[v6];
    [v6][b7]overlay=120:540:shortest=1[v7];
    [v7][b8]overlay=120:615:shortest=1[v8];
    [v8][b9]overlay=120:690:shortest=1[v9];
    [v9][b10]overlay=120:765:shortest=1[v10];
    [v10][b11]overlay=120:840:shortest=1[out]
  " \
  -map "[out]" -map 0:a -c:v libx264 -preset fast -crf 18 -c:a aac -b:a 320k "$OUTPUT_STREAM"

echo "=== Processing abgeschlossen! Video gespeichert unter: ==="
echo "$OUTPUT_STREAM"
