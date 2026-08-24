#!/bin/bash
# SAF V1.9 True Fractal Plasma Engine (Animierter 3D-Mandelbrot & CRF 19)
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

# 2. Exakte Suche nach der echten 3D-Mandelbrot / Omakoma Grafik (V1.3 - V1.6 3D-Ansicht)
BASE_IMAGE=$(python3 -c '
import os
desktop = os.path.expanduser("~/Desktop")
candidates = []
for root, dirs, files in os.walk(desktop):
    for f in files:
        if f.endswith(".png") and ("3D" in f or "Integrierte" in f or "Abbildung" in f) and not "Feature" in f:
            candidates.append(os.path.join(root, f))
if candidates:
    print(candidates[0])
')

if [ -z "$BASE_IMAGE" ]; then
    BASE_IMAGE="$SAF_DIR/V 1.6 INTEGRIERTE SAF-SPEKTRALANALYSE & FARBMAPPING - 3D ANSICHT.png"
fi

echo "=== Echte Fraktal-3D-Grafik geladen: $BASE_IMAGE ==="

OUTPUT_STREAM="$SAF_DIR/compressed/saf_v1_9_true_fractal_plasma.mp4"
mkdir -p "$(dirname "$OUTPUT_STREAM")"

# 3. FFmpeg Rendering: Lebendige Plasmabewegung auf dem echten Fraktal + Spektral-Panels + CRF 19
echo "=== Starte True Fractal Plasma Animation (CRF 19) ==="
ffmpeg -y -i "$TARGET_AUDIO" -loop 1 -i "$BASE_IMAGE" \
  -filter_complex "
    [0:a]asplit=5[a_wif][a_mif][a_hif][a_phase][a_out];

    [1:v]scale=1920:1080:force_original_aspect_ratio=decrease,
         pad=1920:1080:(ow-iw)/2:(oh-ih)/2,
         zoompan=z='1.002+0.0008*sin(2*PI*time/2.5)':x='(iw-iw/zoom)/2+10*sin(2*PI*time/4)':y='(ih-ih/zoom)/2+10*cos(2*PI*time/4)':d=1:s=1920x1080:fps=60,
         lenscorrection=cx=0.5:cy=0.5:k1=-0.22:k2=0.08,
         hue=h='15*sin(2*PI*t/5)':s=1.6,
         gblur=sigma=0.15:steps=1[bg_fractal_plasma];

    [a_wif]lowpass=f=200,showfreqs=s=300x120:mode=bar:cmode=separate:colors=red|orange[wif_panel];
    [wif_panel]drawbox=x=0:y=0:w=iw:h=ih:color=0xff4500@0.8:t=3[wif_frame];

    [a_mif]bandpass=f=1000:width_type=h:w=800,showfreqs=s=300x120:mode=bar:cmode=separate:colors=yellow|green[mif_panel];
    [mif_panel]drawbox=x=0:y=0:w=iw:h=ih:color=0x32cd32@0.8:t=3[mif_frame];

    [a_hif]highpass=f=3000,showfreqs=s=300x120:mode=bar:cmode=separate:colors=cyan|blue[hif_panel];
    [hif_panel]drawbox=x=0:y=0:w=iw:h=ih:color=0x00ffff@0.8:t=3[hif_frame];

    [a_phase]showwaves=s=1800x120:mode=line:colors=0x00ffff@0.9|0xff00ff@0.9|0xffff00@0.9[phase_stream];
    [phase_stream]drawbox=x=0:y=0:w=iw:h=ih:color=0xffffff@0.6:t=2[phase_panel];

    [bg_fractal_plasma][wif_frame]overlay=30:30:shortest=1[v_stage1];
    [v_stage1][mif_frame]overlay=30:160:shortest=1[v_stage2];
    [v_stage2][hif_frame]overlay=30:290:shortest=1[v_stage3];
    [v_stage3][phase_panel]overlay=(W-w)/2:H-h-20:shortest=1[out]
  " \
  -map "[out]" -map "[a_out]" -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -c:a aac -b:a 256k -shortest "$OUTPUT_STREAM"

echo "=== Rendering erfolgreich! Output: $OUTPUT_STREAM ==="
