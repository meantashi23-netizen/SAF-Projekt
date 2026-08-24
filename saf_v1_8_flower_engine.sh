#!/bin/bash
# SAF V1.8 Flower of Life & Frequency Band Interference Engine
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
    echo "Synthesisiere SAF V1.8 Flower-Carrier Signal..."
    AUDIO_INPUT="$SAF_DIR/saf_v18_flower_carrier.wav"
    ffmpeg -y -f lavfi -i "eval=val=sin(2*PI*1.5*t)+0.4*sin(2*PI*8*t)+0.3*sin(2*PI*60*t)+0.2*sin(2*PI*1.368*t):s=44100:d=10" "$AUDIO_INPUT" -loglevel error
fi

OUTPUT_STREAM="$SAF_DIR/saf_v1_8_flower_matrix.mp4"

echo "=== SAF V1.8 Flower of Life Engine Pipeline gestartet ==="
echo "=== Audioquelle: $AUDIO_INPUT ==="

ffmpeg -y -i "$AUDIO_INPUT" -f lavfi -i "mandelbrot=s=1920x1080:maxiter=2500:start_x=-0.743643887037:start_y=0.131825904205" \
  -filter_complex "
    [0:a]asplit=5[a_wif][a_mif][a_hif][a_phase][a_out];

    [1:v]format=yuv420p,
         zoompan=z='1.001+0.0006*sin(2*PI*time/1.368)':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:s=1920x1080:fps=60,
         lenscorrection=cx=0.5:cy=0.4:k1=-0.28:k2=0.10,
         hue=h='160+50*sin(2*PI*t/3.1415)':s=2.7,
         perspective=x0=W*0.06:y0=H*0.20:x1=W*0.94:y1=H*0.08:x2=W*0.02:y2=H*0.94:x3=W*0.98:y3=H*0.85:interpolation=1,
         gblur=sigma=0.3:steps=1,
         unsharp=3:3:0.9[bg_flower_mesh];

    [a_wif]lowpass=f=200,showfreqs=s=300x120:mode=bar:cmode=separate:colors=red|orange[wif_panel];
    [wif_panel]drawbox=x=0:y=0:w=iw:h=ih:color=0xff4500@0.8:t=1[wif_frame];

    [a_mif]bandpass=f=1000:width_type=h:w=800,showfreqs=s=300x120:mode=bar:cmode=separate:colors=yellow|green[mif_panel];
    [mif_panel]drawbox=x=0:y=0:w=iw:h=ih:color=0x32cd32@0.8:t=1[mif_frame];

    [a_hif]highpass=f=3000,showfreqs=s=300x120:mode=bar:cmode=separate:colors=cyan|blue[hif_panel];
    [hif_panel]drawbox=x=0:y=0:w=iw:h=ih:color=0x00ffff@0.8:t=1[hif_frame];

    [a_phase]showwaves=s=1800x120:mode=line:colors=0x00ffff@0.9|0xff00ff@0.9|0xffff00@0.9[phase_stream];
    [phase_stream]drawbox=x=0:y=0:w=iw:h=ih:color=0xffffff@0.6:t=1[phase_panel];

    [bg_flower_mesh][wif_frame]overlay=30:30:shortest=1[v_stage1];
    [v_stage1][mif_frame]overlay=30:160:shortest=1[v_stage2];
    [v_stage2][hif_frame]overlay=30:290:shortest=1[v_stage3];
    [v_stage3][phase_panel]overlay=(W-w)/2:H-h-20:shortest=1[out]
  " \
  -map "[out]" -map "[a_out]" -c:v libx264 -preset slow -crf 13 -pix_fmt yuv420p -c:a aac -b:a 320k "$OUTPUT_STREAM"

echo "=== SAF V1.8 Flower Engine Rendering erfolgreich abgeschlossen! Output: $OUTPUT_STREAM ==="
