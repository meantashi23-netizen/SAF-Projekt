#!/bin/bash
# SAF OMAKOMA Tripleslit (Dreifachspalt) Spectral Engine - Fixed Syntax

SAF_DIR="$HOME/Desktop/5D-SAF Set/Video & π5"
AUDIO_NAME="Recording_2026-07-30_01h50m56s.wav"

# 1. Audioquelle orten
if [ -f "$SAF_DIR/$AUDIO_NAME" ]; then
    AUDIO_INPUT="$SAF_DIR/$AUDIO_NAME"
elif [ -d "$SAF_DIR" ]; then
    AUDIO_INPUT=$(ls -t "$SAF_DIR"/*.wav 2>/dev/null | head -n 1)
fi

OUTPUT_STREAM="$SAF_DIR/saf_omakoma_tripleslit_matrix.mp4"

if [ -z "$AUDIO_INPUT" ] || [ ! -f "$AUDIO_INPUT" ]; then
    echo "Fehler: Keine .wav Audioquelle im SAF-Ordner gefunden!"
    exit 1
fi

echo "=== SAF OMAKOMA Tripleslit Pipeline gestartet ==="
echo "=== Audioquelle: $AUDIO_INPUT ==="

# Mandelbrot-Syntax korrigiert (ohne ungültige 'side' Option)
ffmpeg -y -i "$AUDIO_INPUT" -f lavfi -i "mandelbrot=s=1920x1080:maxiter=200:start_x=-0.74:start_y=0.13" \
  -filter_complex "
    [1:v]format=yuv420p,hue=h=90:s=1.5[bg_fractal];
    
    [0:a]lowpass=f=120,showwaves=s=1200x400:mode=cline:colors=0xff0055@0.8[wave_center];
    [0:a]bandpass=f=1000:width_type=h:w=1200,showwaves=s=1200x400:mode=cline:colors=0x00ffff@0.7[wave_left];
    [0:a]highpass=f=4000,showwaves=s=1200x400:mode=cline:colors=0xff00cc@0.7[wave_right];

    [wave_left]rotate=-30*PI/180:ow=hypot(iw\,ih):oh=ow:c=none[slit1];
    [wave_right]rotate=30*PI/180:ow=hypot(iw\,ih):oh=ow:c=none[slit2];

    [bg_fractal][slit1]overlay=(W-w)/2-300:(H-h)/2:shortest=1[v1];
    [v1][slit2]overlay=(W-w)/2+300:(H-h)/2:shortest=1[v2];
    [v2][wave_center]overlay=(W-w)/2:(H-h)/2:shortest=1[out]
  " \
  -map "[out]" -map 0:a -c:v libx264 -preset fast -crf 18 -c:a aac -b:a 320k "$OUTPUT_STREAM"

echo "=== OMAKOMA Rendering erfolgreich! Video gespeichert unter: ==="
echo "$OUTPUT_STREAM"
