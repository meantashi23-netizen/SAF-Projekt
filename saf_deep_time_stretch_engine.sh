#!/bin/bash
# SAF Deep-Zoom & Time-Stretch (Audio x0.333333 / 3x Duration + OMAKOMA Tripleslit) - Fixed Filtergraph

SAF_DIR="$HOME/Desktop/5D-SAF Set/Video & π5"
AUDIO_NAME="Recording_2026-07-30_01h50m56s.wav"

# 1. Audio-Eingang finden
if [ -f "$SAF_DIR/$AUDIO_NAME" ]; then
    AUDIO_INPUT="$SAF_DIR/$AUDIO_NAME"
elif [ -d "$SAF_DIR" ]; then
    AUDIO_INPUT=$(ls -t "$SAF_DIR"/*.wav 2>/dev/null | head -n 1)
fi

OUTPUT_STREAM="$SAF_DIR/saf_omakoma_timestretch_3x.mp4"

if [ -z "$AUDIO_INPUT" ] || [ ! -f "$AUDIO_INPUT" ]; then
    echo "Fehler: Keine .wav Audioquelle im SAF-Ordner gefunden!"
    exit 1
fi

echo "=== SAF Time-Stretch (0.333x) & Deep-Zoom Pipeline gestartet ==="
echo "=== Audioquelle: $AUDIO_INPUT ==="

# FFmpeg Rendering mit asplit für saubere Audio-Verzweigung
ffmpeg -y -i "$AUDIO_INPUT" -f lavfi -i "mandelbrot=s=1920x1080:maxiter=500:start_x=-0.743643887037:start_y=0.131825904205" \
  -filter_complex "
    [0:a]asetrate=44100*0.333333333333,aresample=44100,asplit=4[a1][a2][a3][a_out];
    
    [1:v]format=yuv420p,hue=h=120:s=1.8,zoompan=z='min(zoom+0.0015,2.5)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080[bg_zoom];
    
    [a1]lowpass=f=120,showwaves=s=1200x400:mode=cline:colors=0xff0055@0.8[wave_center];
    [a2]bandpass=f=600:width_type=h:w=800,showwaves=s=1200x400:mode=cline:colors=0x00ffff@0.7[wave_left];
    [a3]highpass=f=2500,showwaves=s=1200x400:mode=cline:colors=0xff00cc@0.7[wave_right];

    [wave_left]rotate=-30*PI/180:ow=hypot(iw\,ih):oh=ow:c=none[slit1];
    [wave_right]rotate=30*PI/180:ow=hypot(iw\,ih):oh=ow:c=none[slit2];

    [bg_zoom][slit1]overlay=(W-w)/2-300:(H-h)/2:shortest=1[v1];
    [v1][slit2]overlay=(W-w)/2+300:(H-h)/2:shortest=1[v2];
    [v2][wave_center]overlay=(W-w)/2:(H-h)/2:shortest=1[out]
  " \
  -map "[out]" -map "[a_out]" -c:v libx264 -preset fast -crf 18 -c:a aac -b:a 320k "$OUTPUT_STREAM"

echo "=== Rendering erfolgreich abgeschlossen! Datei liegt unter: ==="
echo "$OUTPUT_STREAM"
