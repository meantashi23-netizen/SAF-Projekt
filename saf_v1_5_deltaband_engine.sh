#!/bin/bash
# SAF V1.5 Delta-Band Integration & Bifurcation Point Mapping

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

# Fallback: Synthesisiere Delta-Band Frequenzen (1.5 Hz + Sub-Carrier), falls keine WAV existiert
if [ -z "$AUDIO_INPUT" ] || [ ! -f "$AUDIO_INPUT" ]; then
    echo "Synthesisiere SAF Delta-Band Frequenz (0.5 - 4 Hz)..."
    AUDIO_INPUT="$SAF_DIR/saf_delta_carrier.wav"
    ffmpeg -y -f lavfi -i "eval=val=sin(2*PI*1.5*t)+0.4*sin(2*PI*3.0*t)+0.2*sin(2*PI*110*t):s=44100:d=10" "$AUDIO_INPUT" -loglevel error
fi

OUTPUT_STREAM="$SAF_DIR/saf_v1_5_deltaband_matrix.mp4"

echo "=== SAF V1.5 Delta-Band Pipeline gestartet ==="
echo "=== Audioquelle: $AUDIO_INPUT ==="

ffmpeg -y -i "$AUDIO_INPUT" -f lavfi -i "mandelbrot=s=1920x1080:maxiter=1800:start_x=-0.743643887037:start_y=0.131825904205" \
  -filter_complex "
    [0:a]asplit=5[a_delta][a_w][a_phi][a_eta][a_out];

    [1:v]format=yuv420p,
         zoompan=z='1.0006+0.0008*on':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:s=1920x1080:fps=60,
         lenscorrection=cx=0.5:cy=0.5:k1=-0.22:k2=0.09,
         hue=h='140+50*sin(2*PI*t/3.8)':s=2.4,
         perspective=x0=W*0.08:y0=H*0.15:x1=W*0.92:y1=H*0.05:x2=W*0.02:y2=H*0.92:x3=W*0.98:y3=H*0.82:interpolation=1,
         gblur=sigma=0.6:steps=1,
         unsharp=3:3:0.5[bg_smoothed];

    /* Delta-Band Spektrum (0.5-4 Hz Fokus) */
    [a_delta]lowpass=f=4,showfreqs=s=450x300:mode=bar:cmode=separate:colors=red|magenta|deepviolet[delta_gui];
    [delta_gui]drawbox=x=0:y=0:w=iw:h=ih:color=0xff0055@0.8:t=2,gblur=sigma=0.8:steps=1[delta_frame];

    /* Bifurkationskaskaden-Oszillation (Zentriertes Feigenbaum-Netzwerk) */
    [a_w]lowpass=f=4,showwaves=s=1000x500:mode=cline:colors=0x00ffff@0.75,rotate=90*PI/180:ow=hypot(iw\,ih):oh=ow:c=none[bifurcation_tree];

    [a_phi]bandpass=f=800:width_type=h:w=600,showwaves=s=1800x120:mode=line:colors=0x00ffcc@0.85[stream_phi];
    [a_eta]highpass=f=3000,showwaves=s=1800x120:mode=line:colors=0xffff00@0.85[stream_eta];

    [stream_phi][stream_eta]overlay=0:0[stream_4d_panel];
    [stream_4d_panel]drawbox=x=0:y=0:w=iw:h=ih:color=0xff00ff@0.5:t=1,gblur=sigma=0.5:steps=1[stream_panel_smoothed];

    /* Compositing Delta-Bifurcation Layer */
    [bg_smoothed][bifurcation_tree]overlay=(W-w)/2:(H-h)/2:shortest=1[v_bif];
    [v_bif][delta_frame]overlay=40:40:shortest=1[v_spec];
    [v_spec][stream_panel_smoothed]overlay=(W-w)/2:H-h-30:shortest=1[out]
  " \
  -map "[out]" -map "[a_out]" -c:v libx264 -preset slow -crf 13 -pix_fmt yuv420p -c:a aac -b:a 320k "$OUTPUT_STREAM"

echo "=== SAF V1.5 Delta-Band Rendering abgeschlossen! Output: $OUTPUT_STREAM ==="
