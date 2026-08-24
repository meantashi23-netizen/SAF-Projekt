#!/bin/bash
# SAF V1.9 Perfect Neon Fractal Engine (Fehlerfrei & CRF 19)
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

# 2. Exakte 4D-Mandelbrot Grafik aus dem SAF-Projekt
BASE_IMAGE="$HOME/Desktop/SAF-Projekt/mandelbrot_4d_output.png"
if [ ! -f "$BASE_IMAGE" ]; then
    BASE_IMAGE=$(python3 -c '
import os
desktop = os.path.expanduser("~/Desktop")
for root, dirs, files in os.walk(desktop):
    for f in files:
        if "mandelbrot_4d_output.png" in f:
            print(os.path.join(root, f))
            break
    else:
        continue
    break
')
fi

if [ -z "$BASE_IMAGE" ] || [ ! -f "$BASE_IMAGE" ]; then
    echo "FEHLER: Fraktal-Grafik mandelbrot_4d_output.png nicht gefunden!"
    exit 1
fi

echo "=== Fraktal-Grafik geladen: $BASE_IMAGE ==="

OUTPUT_STREAM="$SAF_DIR/compressed/saf_v1_9_perfect_neon_fractal.mp4"
mkdir -p "$(dirname "$OUTPUT_STREAM")"

# 3. FFmpeg Rendering mit absolut sicheren, kurzen Zeilen
echo "=== Starte Perfect Neon Fractal Rendering (CRF 19) ==="
ffmpeg -y -i "$TARGET_AUDIO" -loop 1 -i "$BASE_IMAGE" \
  -filter_complex "
    [0:a]asplit=5[a_wif][a_mif][a_hif][a_phase][a_out];

    [1:v]scale=1920:1080:force_original_aspect_ratio=increase,
         crop=1920:1080,
         zoompan=z='1.002+0.0006*sin(2*PI*time/3.0)':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:s=1920x1080:fps=60,
         hue=h='25*sin(2*PI*t/6)':s=1.8[bg_neon];

    [a_wif]lowpass=f=200,showfreqs=s=280x110:mode=bar:cmode=separate:colors=red|orange[wif_s];
    [wif_s]drawbox=x=0:y=0:w=iw:h=ih:color=0xff4500@0.85:t=2[wif_panel];

    [a_mif]bandpass=f=1000:width_type=h:w=800,showfreqs=s=280x110:mode=bar:cmode=separate:colors=yellow|green[mif_s];
    [mif_s]drawbox=x=0:y=0:w=iw:h=ih:color=0x32cd32@0.85:t=2[mif_panel];

    [a_hif]highpass=f=3000,showfreqs=s=280x110:mode=bar:cmode=separate:colors=cyan|blue[hif_s];
    [hif_s]drawbox=x=0:y=0:w=iw:h=ih:color=0x00ffff@0.85:t=2[hif_panel];

    [a_phase]showwaves=s=1800x90:mode=line:colors=0x00ffff@0.9|0xff00ff@0.9|0xffff00@0.9[phase_s];
    [phase_s]drawbox=x=0:y=0:w=iw:h=ih:color=0xffffff@0.6:t=2[phase_panel];

    [bg_neon][wif_panel]overlay=35:35:shortest=1[v1];
    [v1][mif_panel]overlay=35:160:shortest=1[v2];
    [v2][hif_panel]overlay=35:285:shortest=1[v3];
    [v3][phase_panel]overlay=(W-w)/2:H-h-15:shortest=1[out]
  " \
  -map "[out]" -map "[a_out]" -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -c:a aac -b:a 256k -shortest "$OUTPUT_STREAM"

echo "=== Fertig! Output gespeichert unter: $OUTPUT_STREAM ==="
