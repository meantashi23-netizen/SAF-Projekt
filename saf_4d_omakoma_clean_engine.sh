#!/bin/bash
# SAF 4D Clean Engine - Dynamic Zoom & Border Artifact Fix

SAF_DIR="$HOME/Desktop/5D-SAF Set/Video & π5"
AUDIO_NAME="Recording_2026-07-30_01h50m56s.wav"

if [ -f "$SAF_DIR/$AUDIO_NAME" ]; then
    AUDIO_INPUT="$SAF_DIR/$AUDIO_NAME"
elif [ -d "$SAF_DIR" ]; then
    AUDIO_INPUT=$(ls -t "$SAF_DIR"/*.wav 2>/dev/null | head -n 1)
fi

OUTPUT_STREAM="$SAF_DIR/saf_4d_omakoma_perfect_zoom.mp4"

if [ -z "$AUDIO_INPUT" ] || [ ! -f "$AUDIO_INPUT" ]; then
    echo "Fehler: Keine .wav Audioquelle gefunden!"
    exit 1
fi

echo "=== SAF Clean 4D & Deep-Zoom Pipeline gestartet ==="

# Render-Pipeline: Over-Sampling (2560x1440) + Crop behebt die Streifen am Rand
# zoompan mit z='1.0+0.001*on' sorgt für durchgehenden Zoom über die gesamte Audio-Länge
ffmpeg -y -i "$AUDIO_INPUT" -f lavfi -i "mandelbrot=s=2560x1440:maxiter=800:start_x=-0.743643887037:start_y=0.131825904205" \
  -filter_complex "
    [0:a]asetrate=44100*0.333333333333,aresample=44100,asplit=4[a1][a2][a3][a_out];
    
    [1:v]format=yuv420p,hue=h=140:s=2.0,
         zoompan=z='1.0+0.001*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=2560x1440,
         perspective=x0=W*0.08:y0=H*0.12:x1=W*0.92:y1=H*0.04:x2=W*0.02:y2=H*0.96:x3=W*0.98:y3=H*0.88:interpolation=linear,
         crop=1920:1080:(2560-1920)/2:(1440-1080)/2[bg_clean_4d];
    
    [a1]lowpass=f=120,showwaves=s=1200x400:mode=cline:colors=0xff0055@0.85[wave_center];
    [a2]bandpass=f=600:width_type=h:w=800,showwaves=s=1200x400:mode=cline:colors=0x00ffff@0.75[wave_left];
    [a3]highpass=f=2500,showwaves=s=1200x400:mode=cline:colors=0xff00cc@0.75[wave_right];

    [wave_left]rotate=-30*PI/180:ow=hypot(iw\,ih):oh=ow:c=none[slit1];
    [wave_right]rotate=30*PI/180:ow=hypot(iw\,ih):oh=ow:c=none[slit2];

    [bg_clean_4d][slit1]overlay=(W-w)/2-300:(H-h)/2:shortest=1[v1];
    [v1][slit2]overlay=(W-w)/2+300:(H-h)/2:shortest=1[v2];
    [v2][wave_center]overlay=(W-w)/2:(H-h)/2:shortest=1[out]
  " \
  -map "[out]" -map "[a_out]" -c:v libx264 -preset fast -crf 17 -c:a aac -b:a 320k "$OUTPUT_STREAM"

echo "=== Rendering sauber abgeschlossen! Datei: $OUTPUT_STREAM ==="
