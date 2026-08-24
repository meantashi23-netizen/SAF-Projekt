#!/bin/bash
# SAF V1.7 Vortex & Multi-Dimensional Coupling Engine (Zoompan Fixed)
set -e

SAF_DIR="$HOME/Desktop/5D-SAF Set/Video & π5"
AUDIO_NAME="Recording_2026-07-30_01h50m56s.wav"

mkdir -p "$SAF_DIR"

if [ -f "$SAF_DIR/$AUDIO_NAME" ]; then
    AUDIO_INPUT="$SAF_DIR/$AUDIO_NAME"
elif [ -d "$SAF_DIR" ]; then
    AUDIO_INPUT=$(ls -t "$SAF_DIR"/*.wav 2>/dev/null | head -n 1)
fi

if [ -z "$AUDIO_INPUT" ] || [ ! -f "$AUDIO_INPUT" ]; then
    AUDIO_INPUT=$(ls -t *.wav 2>/dev/null | head -n 1)
fi

if [ -z "$AUDIO_INPUT" ] || [ ! -f "$AUDIO_INPUT" ]; then
    echo "Synthesisiere SAF V1.7 Vortex Carrier Signal..."
    AUDIO_INPUT="$SAF_DIR/saf_v17_vortex_carrier.wav"
    ffmpeg -y -f lavfi -i "eval=val=sin(2*PI*1.5*t)+0.4*sin(2*PI*4.6692*t)+0.3*sin(2*PI*11*t):s=44100:d=10" "$AUDIO_INPUT" -loglevel error
fi

OUTPUT_STREAM="$SAF_DIR/saf_v1_7_vortex_matrix.mp4"

echo "=== SAF V1.7 Vortex Engine Pipeline gestartet ==="
echo "=== Audioquelle: $AUDIO_INPUT ==="

ffmpeg -y -i "$AUDIO_INPUT" -f lavfi -i "mandelbrot=s=1920x1080:maxiter=2500:start_x=-0.743643887037:start_y=0.131825904205" \
  -filter_complex "
    [0:a]asplit=5[a_delta][a_feig][a_n11][a_gparam][a_out];

    [1:v]format=yuv420p,
         zoompan=z='1.001+0.0005*sin(2*PI*time/4.6692)':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:s=1920x1080:fps=60,
         lenscorrection=cx=0.5:cy=0.3:k1=-0.35:k2=0.15,
         hue=h='180+40*sin(2*PI*t/2.5029)':s=2.8,
         perspective=x0=W*0.05:y0=H*0.25:x1=W*0.95:y1=H*0.10:x2=W*0.01:y2=H*0.95:x3=W*0.99:y3=H*0.88:interpolation=1,
         gblur=sigma=0.4:steps=1,
         unsharp=3:3:0.9[bg_vortex_mesh];

    [a_delta]lowpass=f=4,showfreqs=s=420x280:mode=bar:cmode=separate:colors=violet|magenta|darkblue|cyan[delta_gui];
    [delta_gui]drawbox=x=0:y=0:w=iw:h=ih:color=0x8b00ff@0.8:t=2,gblur=sigma=0.6:steps=1[delta_frame];

    [a_feig]lowpass=f=11,showwaves=s=1200x400:mode=cline:colors=0xff00ff@0.85,rotate=180*PI/180:ow=hypot(iw\,ih):oh=ow:c=none[torus_grid];

    [a_n11]bandpass=f=110:width_type=h:w=22,showwaves=s=320x200:mode=line:colors=0x00ffff@0.9[n11_panel];
    [n11_panel]drawbox=x=0:y=0:w=iw:h=ih:color=0x00ffff@0.8:t=2[n11_frame];

    [a_gparam]highpass=f=2000,showwaves=s=1800x100:mode=line:colors=0xffaa00@0.85[g_stream];
    [g_stream]drawbox=x=0:y=0:w=iw:h=ih:color=0xffaa00@0.5:t=1[g_panel];

    [bg_vortex_mesh][torus_grid]overlay=(W-w)/2:0:shortest=1[v_torus];
    [v_torus][delta_frame]overlay=40:40:shortest=1[v_delta];
    [v_delta][n11_frame]overlay=1550:100:shortest=1[v_n11];
    [v_n11][g_panel]overlay=(W-w)/2:H-h-20:shortest=1[out]
  " \
  -map "[out]" -map "[a_out]" -c:v libx264 -preset slow -crf 13 -pix_fmt yuv420p -c:a aac -b:a 320k "$OUTPUT_STREAM"

echo "=== SAF V1.7 Vortex Rendering erfolgreich abgeschlossen! Output: $OUTPUT_STREAM ==="
