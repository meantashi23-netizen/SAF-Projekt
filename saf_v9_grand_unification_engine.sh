#!/bin/bash
# SAF V9.0 Grand Unification Engine
# Integrates: Julia Set Fold Modulation, Hyper-Spectral Data Cubes & GUC V1.0

SAF_DIR="$HOME/Desktop/5D-SAF Set/Video & π5"
AUDIO_NAME="Recording_2026-07-30_01h50m56s.wav"

if [ -f "$SAF_DIR/$AUDIO_NAME" ]; then
    AUDIO_INPUT="$SAF_DIR/$AUDIO_NAME"
elif [ -d "$SAF_DIR" ]; then
    AUDIO_INPUT=$(ls -t "$SAF_DIR"/*.wav 2>/dev/null | head -n 1)
fi

# Fallback: Falls Datei im aktuellen Ordner liegt
if [ -z "$AUDIO_INPUT" ] || [ ! -f "$AUDIO_INPUT" ]; then
    AUDIO_INPUT=$(ls -t *.wav 2>/dev/null | head -n 1)
fi

OUTPUT_STREAM="$SAF_DIR/saf_v9_grand_unification_matrix.mp4"

if [ -z "$AUDIO_INPUT" ] || [ ! -f "$AUDIO_INPUT" ]; then
    echo "Fehler: Keine .wav Audioquelle im SAF-Ordner gefunden!"
    exit 1
fi

echo "=== SAF V9.0 Grand Unification Pipeline gestartet ==="
echo "=== Audioquelle: $AUDIO_INPUT ==="

ffmpeg -y -i "$AUDIO_INPUT" -f lavfi -i "mandelbrot=s=1920x1080:maxiter=1600:start_x=-0.743643887037:start_y=0.131825904205" \
  -filter_complex "
    [0:a]asplit=6[a1][a2][a3][a4][a5][a_out];

    [1:v]format=yuv420p,
         zoompan=z='1.0006+0.0008*on':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:s=1920x1080:fps=60,
         lenscorrection=cx=0.5:cy=0.5:k1=-0.20:k2=0.08,
         hue=h='100+45*sin(2*PI*t/3.8)':s=2.5,
         curves=all='0/0 0.25/0.15 0.5/0.65 0.75/0.85 1/1'[bg_fold_modulation];

    [a1]lowpass=f=90,showwaves=s=1200x350:mode=cline:colors=0xff0033@0.85[cube_red];
    [a2]bandpass=f=300:width_type=h:w=250,showwaves=s=1200x350:mode=cline:colors=0xff9900@0.85[cube_orange];
    [a3]bandpass=f=1200:width_type=h:w=800,showwaves=s=1200x350:mode=cline:colors=0x33ff00@0.85[cube_green];
    [a4]bandpass=f=3500:width_type=h:w=2000,showwaves=s=1200x350:mode=cline:colors=0x00ffff@0.85[cube_cyan];
    [a5]highpass=f=8000,showwaves=s=1200x350:mode=cline:colors=0xcc00ff@0.85[cube_violet];

    [cube_orange]rotate=-90*PI/180:ow=hypot(iw\,ih):oh=ow:c=none[slit_pi2_left];
    [cube_cyan]rotate=90*PI/180:ow=hypot(iw\,ih):oh=ow:c=none[slit_pi2_right];
    [cube_violet]rotate=45*PI/180:ow=hypot(iw\,ih):oh=ow:c=none[slit_diag];

    [bg_fold_modulation][slit_pi2_left]overlay=(W-w)/2-400:(H-h)/2:shortest=1[v1];
    [v1][slit_pi2_right]overlay=(W-w)/2+400:(H-h)/2:shortest=1[v2];
    [v2][slit_diag]overlay=(W-w)/2:(H-h)/2:shortest=1[v3];
    [v3][cube_green]overlay=(W-w)/2:(H-h)/2+200:shortest=1[v4];
    [v4][cube_red]overlay=(W-w)/2:(H-h)/2-200:shortest=1[out]
  " \
  -map "[out]" -map "[a_out]" -c:v libx264 -preset slow -crf 13 -pix_fmt yuv420p -c:a aac -b:a 320k "$OUTPUT_STREAM"

echo "=== SAF V9.0 Grand Unification Rendering abgeschlossen! ==="
echo "Output liegt unter: $OUTPUT_STREAM"
