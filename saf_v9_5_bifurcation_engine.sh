#!/bin/bash
# SAF V9.5 Spektral-Bifurkations Engine
# Integrates: 3D Bifurcation Surface, 2D Spectrum Analyzer & 4D Continuity Stream (Omakoma)

SAF_DIR="$HOME/Desktop/5D-SAF Set/Video & π5"
AUDIO_NAME="Recording_2026-07-30_01h50m56s.wav"

if [ -f "$SAF_DIR/$AUDIO_NAME" ]; then
    AUDIO_INPUT="$SAF_DIR/$AUDIO_NAME"
elif [ -d "$SAF_DIR" ]; then
    AUDIO_INPUT=$(ls -t "$SAF_DIR"/*.wav 2>/dev/null | head -n 1)
fi

if [ -z "$AUDIO_INPUT" ] || [ ! -f "$AUDIO_INPUT" ]; then
    AUDIO_INPUT=$(ls -t *.wav 2>/dev/null | head -n 1)
fi

OUTPUT_STREAM="$SAF_DIR/saf_v9_5_bifurcation_matrix.mp4"

if [ -z "$AUDIO_INPUT" ] || [ ! -f "$AUDIO_INPUT" ]; then
    echo "Fehler: Keine .wav Audioquelle gefunden!"
    exit 1
fi

echo "=== SAF V9.5 Spektral-Bifurkations Pipeline gestartet ==="
echo "=== Audioquelle: $AUDIO_INPUT ==="

ffmpeg -y -i "$AUDIO_INPUT" -f lavfi -i "mandelbrot=s=1920x1080:maxiter=1600:start_x=-0.743643887037:start_y=0.131825904205" \
  -filter_complex "
    [0:a]asplit=5[a_spec][a_w][a_phi][a_eta][a_out];

    /* 1. Haupt-Mandelbrot / Julia Base + G-Hutabaci Warp + Bifurkations-Colorization */
    [1:v]format=yuv420p,
         zoompan=z='1.0006+0.0008*on':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:s=1920x1080:fps=60,
         lenscorrection=cx=0.5:cy=0.5:k1=-0.22:k2=0.09,
         hue=h='140+50*sin(2*PI*t/3.8)':s=2.4,
         perspective=x0=W*0.08:y0=H*0.15:x1=W*0.92:y1=H*0.05:x2=W*0.02:y2=H*0.92:x3=W*0.98:y3=H*0.82:interpolation=1[bg_bifurcation];

    /* 2. 2D Spectrum Analysis Overlay (Links oben - KAF/SAF Analyze GUI) */
    [a_spec]showfreqs=s=450x300:mode=bar:cmode=separate:colors=red|yellow|green|cyan|magenta[spec_gui];
    [spec_gui]drawbox=x=0:y=0:w=iw:h=ih:color=0x00ffff@0.6:t=2[spec_frame];

    /* 3. 4D Kontinuitäts-Stream (Omakoma Oszillations-Tracker unten) */
    [a_w]lowpass=f=200,showwaves=s=1800x120:mode=line:colors=0xff0055@0.85[stream_w];
    [a_phi]bandpass=f=800:width_type=h:w=600,showwaves=s=1800x120:mode=line:colors=0x00ffcc@0.85[stream_phi];
    [a_eta]highpass=f=3000,showwaves=s=1800x120:mode=line:colors=0xffff00@0.85[stream_eta];

    [stream_w][stream_phi]overlay=0:0[stream_12];
    [stream_12][stream_eta]overlay=0:0[stream_4d_panel];
    [stream_4d_panel]drawbox=x=0:y=0:w=iw:h=ih:color=0xff00ff@0.5:t=1[stream_panel_framed];

    /* 4. Compositing aller V1.2 Layer */
    [bg_bifurcation][spec_frame]overlay=40:40:shortest=1[v_spec];
    [v_spec][stream_panel_framed]overlay=(W-w)/2:H-h-30:shortest=1[out]
  " \
  -map "[out]" -map "[a_out]" -c:v libx264 -preset slow -crf 13 -pix_fmt yuv420p -c:a aac -b:a 320k "$OUTPUT_STREAM"

echo "=== SAF V9.5 Bifurkations-Rendering abgeschlossen! ==="
echo "Output liegt unter: $OUTPUT_STREAM"
