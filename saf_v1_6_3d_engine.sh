#!/bin/bash
# SAF V1.6 3D-Ansicht Engine (Robust & CRF 19)
set -e

SAF_DIR="$HOME/Desktop/5D-SAF Set/Video & π5"
OUTPUT_DIR="$SAF_DIR/compressed"
mkdir -p "$OUTPUT_DIR"

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

# 2. Exakter Pfad zur V1.6 Grafik (direkt aus deinem Finder-Ordner)
BASE_IMAGE="$SAF_DIR/V 1.6 INTEGRIERTE SAF-SPEKTRALANALYSE & FARBMAPPING - 3D ANSICHT.png"

if [ ! -f "$BASE_IMAGE" ]; then
    # Fallback Suche
    BASE_IMAGE=$(find "$SAF_DIR" -name "*V 1.6*3D ANSICHT.png" | head -n 1)
fi

if [ -z "$BASE_IMAGE" ] || [ ! -f "$BASE_IMAGE" ]; then
    echo "FEHLER: V 1.6 Grafik wurde nicht gefunden!"
    exit 1
fi

echo "=== 3D-Ansicht V1.6 Textur geladen: $BASE_IMAGE ==="
OUTPUT_MP4="$OUTPUT_DIR/saf_v1_6_3d_spectral_matrix.mp4"

# 3. FFmpeg Rendering mit sauber escapten Variablen
echo "=== Starte SAF V1.6 3D-Rendering (CRF 19) ==="
ffmpeg -y -i "$TARGET_AUDIO" -loop 1 -i "$BASE_IMAGE" \
  -filter_complex "
    [0:a]asplit=4[a_wif][a_mif][a_hif][a_out];

    [1:v]scale=1920:1080:force_original_aspect_ratio=decrease,
         pad=1920:1080:(ow-iw)/2:(oh-ih)/2,
         zoompan=z='1.002+0.0005*sin(2*PI*time/3.0)':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:s=1920x1080:fps=60,
         hue=h='10*sin(2*PI*t/8)':s=1.3[bg_3d];

    [a_wif]lowpass=f=250,showfreqs=s=320x130:mode=bar:cmode=separate:colors=red|orange[wif_panel];
    [wif_panel]drawbox=x=0:y=0:w=iw:h=ih:color=0xff4500@0.85:t=3[wif_frame];

    [a_mif]bandpass=f=1200:width_type=h:w=900,showfreqs=s=320x130:mode=bar:cmode=separate:colors=yellow|green[mif_panel];
    [mif_panel]drawbox=x=0:y=0:w=iw:h=ih:color=0x32cd32@0.85:t=3[mif_frame];

    [a_hif]highpass=f=3500,showfreqs=s=320x130:mode=bar:cmode=separate:colors=cyan|blue[hif_panel];
    [hif_panel]drawbox=x=0:y=0:w=iw:h=ih:color=0x00ffff@0.85:t=3[hif_frame];

    [bg_3d][wif_frame]overlay=40:40:shortest=1[v_stage1];
    [v_stage1][mif_panel]overlay=40:190:shortest=1[v_stage2];
    [v_stage2][hif_panel]overlay=40:340:shortest=1[out]
  " \
  -map "[out]" -map "[a_out]" -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -c:a aac -b:a 256k -shortest "$OUTPUT_MP4"

echo "=== Rendering erfolgreich abgeschlossen! Datei gespeichert unter: $OUTPUT_MP4 ==="
