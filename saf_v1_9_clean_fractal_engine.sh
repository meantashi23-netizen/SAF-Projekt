#!/bin/bash
# SAF V1.9 Clean Professional Fractal Engine (CRF 19)
set -e

SAF_DIR="$HOME/Desktop/5D-SAF Set/Video & π5"
mkdir -p "$SAF_DIR"

# 1. Exakte Audioquelle per Python FS-Walker ermitteln
TARGET_AUDIO=$(python3 -c '
import os
desktop = os.path.expanduser("~/Desktop")
for root, dirs, files in os.walk(desktop):
    if "Mean" in root and "Tashi" in root:
        for f in files:
            if "192302" in f and f.endswith(".aif"):
                print(os.path.join(root, f))
                break
')

if [ -z "$TARGET_AUDIO" ] || [ ! -f "$TARGET_AUDIO" ]; then
    echo "FEHLER: Audio-Datei konnte nicht gefunden werden."
    exit 1
fi

echo "=== Audioquelle geladen: $TARGET_AUDIO ==="

# 2. Exakte 3D-Mandelbrot Grafik ermitteln
BASE_IMAGE="$SAF_DIR/saf_3d_mandelbrot.png"
if [ ! -f "$BASE_IMAGE" ]; then
    BASE_IMAGE=$(python3 -c '
import os
desktop = os.path.expanduser("~/Desktop")
for root, dirs, files in os.walk(desktop):
    for f in files:
        if "saf_3d" in f and f.endswith(".png"):
            print(os.path.join(root, f))
            break
    else:
        continue
    break
')
fi

if [ -z "$BASE_IMAGE" ] || [ ! -f "$BASE_IMAGE" ]; then
    echo "FEHLER: 3D Mandelbrot Grafik nicht gefunden!"
    exit 1
fi

echo "=== Saubere Fraktal-Grafik geladen: $BASE_IMAGE ==="

OUTPUT_STREAM="$SAF_DIR/compressed/saf_v1_9_clean_fractal.mp4"
mkdir -p "$(dirname "$OUTPUT_STREAM")"

# 3. FFmpeg Rendering: Schwarzer Hintergrund, sanfter Zoom, saubere Panels
echo "=== Starte Clean Fractal Rendering (CRF 19) ==="
ffmpeg -y -i "$TARGET_AUDIO" -loop 1 -i "$BASE_IMAGE" \
  -filter_complex "
    [0:a]asplit=5[a_wif][a_mif][a_hif][a_phase][a_out];

    # Hintergrund schwarz generieren, 3D-Grafik einpassen und weißer Hintergrund per colorkey entfernen
    [1:v]scale=1200:-1,colorkey=white:0.1:0.1[fg_fractal];
    
    color=c=black:s=1920x1080,fps=60[canvas];
    [canvas][fg_fractal]overlay=(W-w)/2:(H-h)/2:shortest=1,
         zoompan=z='1.001+0.0004*sin(2*PI*time/3.0)':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:s=1920x1080:fps=60[bg_clean];

    [a_wif]lowpass=f=200,showfreqs=s=280=110:mode=bar:cmode=separate:colors=red|orange[wif_panel];
    [wif_panel]drawbox=x=0:y=0:w=iw:h=ih:color=0xff4500@0.85:t=2[wif_frame];

    [a_mif]bandpass=f=1000:width_type=h:w=800,showfreqs=s=280=110:mode=bar:cmode=separate:colors=yellow|green[mif_panel];
    [mif_panel]drawbox=x=0:y=0:w=iw:h=ih:color=0x32cd32@0.85:t=2[mif_frame];

    [a_hif]highpass=f=3000,showfreqs=s=280=110:mode=bar:cmode=separate:colors=cyan|blue[hif_panel];
    [hif_panel]drawbox=x=0:y=0:w=iw:h=ih:color=0x00ffff@0.85:t=2[hif_frame];

    [a_phase]showwaves=s=1800x100:mode=line:colors=0x00ffff@0.9|0xff00ff@0.9|0xffff00@0.9[phase_stream];
    [phase_stream]drawbox=x=0:y=0:w=iw:h=ih:color=0xffffff@0.6:t=2[phase_panel];

    [bg_clean][wif_frame]overlay=40:40:shortest=1[v_stage1];
    [v_stage1][mif_panel]overlay=40:170:shortest=1[v_stage2];
    [v_stage2][hif_panel]overlay=40:300:shortest=1[v_stage3];
    [v_stage3][phase_panel]overlay=(W-w)/2:H-h-20:shortest=1[out]
  " \
  -map "[out]" -map "[a_out]" -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -c:a aac -b:a 256k -shortest "$OUTPUT_STREAM"

echo "=== Fertig! Output: $OUTPUT_STREAM ==="
