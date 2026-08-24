#!/bin/bash
# SAF V1.6 Ultra Spektral-Analyse & Complex Axis Mapping Engine
# Integration: Multi-level Lattice + V1.6 Deep Violet Bands + Node Fusion

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

# Fallback: Synthesisiere SAF Delta/Alpha/Deep-Violet Multi-Carrier Signal
if [ -z "$AUDIO_INPUT" ] || [ ! -f "$AUDIO_INPUT" ]; then
    echo "Synthesisiere SAF V1.6 Ultra Spektral-Träger..."
    AUDIO_INPUT="$SAF_DIR/saf_v16_ultra_carrier.wav"
    ffmpeg -y -f lavfi -i "eval=val=sin(2*PI*1.5*t)+0.5*sin(2*PI*8*t)+0.3*sin(2*PI*60*t)+0.2*sin(2*PI*120*t):s=44100:d=10" "$AUDIO_INPUT" -loglevel error
fi

OUTPUT_STREAM="$SAF_DIR/saf_v1_6_ultra_bifurcation_matrix.mp4"

echo "=== SAF V1.6 Ultra Fusion Pipeline gestartet ==="
echo "=== Audioquelle: $AUDIO_INPUT ==="

ffmpeg -y -i "$AUDIO_INPUT" -f lavfi -i "mandelbrot=s=1920x1080:maxiter=2200:start_x=-0.743643887037:start_y=0.131825904205" \
  -filter_complex "
    [0:a]asplit=5[a_delta][a_w][a_phi][a_eta][a_out];

    [1:v]format=yuv420p,
         zoompan=z='1.0006+0.0008*on':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:s=1920x1080:fps=60,
         lenscorrection=cx=0.5:cy=0.5:k1=-0.22:k2=0.09,
         hue=h='150+60*sin(2*PI*t/3.8)':s=2.6,
         perspective=x0=W*0.08:y0=H*0.15:x1=W*0.92:y1=H*0.05:x2=W*0.02:y2=H*0.92:x3=W*0.98:y3=H*0.82:interpolation=1,
         gblur=sigma=0.5:steps=1,
         unsharp=3:3:0.8[bg_v16_base];

    [a_delta]lowpass=f=4,showfreqs=s=420x280:mode=bar:cmode=separate:colors=violet|magenta|darkblue|cyan[delta_gui];
    [delta_gui]drawbox=x=0:y=0:w=iw:h=ih:color=0x8b00ff@0.8:t=2,gblur=sigma=0.6:steps=1[delta_frame_v16];

    [a_w]lowpass=f=12,showwaves=s=280x180:mode=line:colors=0x00ffff@0.9[sub_graph_a];
    [sub_graph_a]drawbox=x=0:y=0:w=iw:h=ih:color=0x00ffff@0.7:t=1[coupling_node_a];

    [a_phi]bandpass=f=800:width_type=h:w=600,showwaves=s=280x180:mode=line:colors=0xff00ff@0.9[sub_graph_b];
    [sub_graph_b]drawbox=x=0:y=0:w=iw:h=ih:color=0xff00ff@0.7:t=1[coupling_node_b];

    [a_eta]highpass=f=2500,showwaves=s=1800x110:mode=line:colors=0x00ffcc@0.85[stream_omakoma];
    [stream_omakoma]drawbox=x=0:y=0:w=iw:h=ih:color=0x8b00ff@0.6:t=1,gblur=sigma=0.4:steps=1[stream_5d_panel];

    [bg_v16_base][delta_frame_v16]overlay=40:40:shortest=1[v_stage1];
    [v_stage1][coupling_node_a]overlay=50:350:shortest=1[v_stage2];
    [v_stage2][coupling_node_b]overlay=1580:60:shortest=1[v_stage3];
    [v_stage3][stream_5d_panel]overlay=(W-w)/2:H-h-30:shortest=1[out]
  " \
  -map "[out]" -map "[a_out]" -c:v libx264 -preset slow -crf 13 -pix_fmt yuv420p -c:a aac -b:a 320k "$OUTPUT_STREAM"

echo "=== SAF V1.6 Ultra Rendering erfolgreich abgeschlossen! Output: $OUTPUT_STREAM ==="
