#!/bin/bash
# SAF V 33.2 Engine – Interaktiver Audio-Fix (N=257, 3320 Iter, SnaP Mod & Topnotch)
set -e

DESKTOP_DIR="$HOME/Desktop"
SAF_DIR="$DESKTOP_DIR/5D-SAF Set/Video & π5"
TMP_SAF_ANALYSE="$SAF_DIR/.analyse_tmp"

mkdir -p "$SAF_DIR"
mkdir -p "$TMP_SAF_ANALYSE"

echo "=================================================="
echo "=== SAF V 33.2 SnaP Engine (N=257 / Iter=3320) ==="
echo "=================================================="

# 1. INTERAKTIVE AUDIO-AUSWAHL (Verhindert doppelte/falsche Audios)
echo ""
echo "Ziehe deine gewünschte Audio-Datei (.aif / .wav) hier in das Terminal-Fenster und drücke ENTER:"
read -r INPUT_AUDIO_PATH

# Anführungszeichen und Freizeichen vom Drag & Drop aufräumen
TARGET_AUDIO=$(echo "$INPUT_AUDIO_PATH" | sed "s/'//g" | sed 's/"//g' | xargs)

if [ -z "$TARGET_AUDIO" ] || [ ! -f "$TARGET_AUDIO" ]; then
    echo "❌ FEHLER: Datei '$TARGET_AUDIO' existiert nicht!"
    exit 1
fi

echo ""
echo "=== ✅ Gewähltes Audio: $TARGET_AUDIO ==="
echo ""

# 2. Transienten / SnaP RMS-Analyse
echo "=== Analysiere Audio-SnaP Transienten... ==="
ffmpeg -y -i "$TARGET_AUDIO" -af "asetnsamples=n=735,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=$TMP_SAF_ANALYSE/rms.txt" -f null - 2>/dev/null

python3 -c "
import math, os
rms_file = os.path.join('$TMP_SAF_ANALYSE', 'rms.txt')
snap_data_file = os.path.join('$TMP_SAF_ANALYSE', 'snap_mod.txt')
with open(rms_file, 'r') as f, open(snap_data_file, 'w') as out:
    for line in f:
        if 'Overall.RMS_level' in line:
            try:
                db = float(line.split('=')[-1].strip())
                linear = math.pow(10, (max(-60, db)) / 20)
                out.write(f'{linear:.6f}\n')
            except: continue
"

# 3. Python Core Matrix
cat << 'PYEOF' > saf_v33_2_core.py
import numpy as np

class SAFV332Core:
    FEIGENBAUM_DELTA = 4.669201609102990
    N_NODES = 257
    MAX_ITER = 3320

    @classmethod
    def generate_bifurcation_matrix(cls):
        indices = np.arange(1, cls.N_NODES + 1)
        return cls.FEIGENBAUM_DELTA * (indices / cls.N_NODES)

if __name__ == "__main__":
    matrix = SAFV332Core.generate_bifurcation_matrix()
    print(f"SAF V 33.2 Core: N={SAFV332Core.N_NODES} Matrix (3320 Iterations)")
PYEOF

python3 saf_v33_2_core.py

# 4. OMAKOMA PNG Overlay suchen
OMAKOMA_IMG=$(python3 -c '
import os
desktop = os.path.expanduser("~/Desktop")
for root, dirs, files in os.walk(desktop):
    for f in files:
        if "Intercept OMAKOMA" in f and f.endswith(".png"):
            print(os.path.join(root, f))
            break
    else: continue
    break
')

# Dynamischen Ausgabennamen anhand des Audio-Dateinamens generieren
AUDIO_NAME=$(basename "$TARGET_AUDIO" | cut -f 1 -d '.')
OUTPUT_STREAM="$SAF_DIR/compressed/saf_v33_2_${AUDIO_NAME}_stream.mp4"

# 5. Multi-Layer FFmpeg Rendering (CRF 19 / Clean Filtergraph)
echo "=== Starte Rendering: $OUTPUT_STREAM ==="

if [ -n "$OMAKOMA_IMG" ] && [ -f "$OMAKOMA_IMG" ]; then
  ffmpeg -y -i "$TARGET_AUDIO" \
    -f lavfi -i "mandelbrot=s=1920x1080:maxiter=3320:start_x=-0.743643887037:start_y=0.131825904205" \
    -loop 1 -i "$OMAKOMA_IMG" \
    -filter_complex "
      [0:a]asplit=5[a_wif][a_mif][a_hif][a_phase][a_out];

      [1:v]format=yuv420p,
           zoompan=z='1.002+0.0008*sin(2*PI*time/1.368)':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:s=1920x1080:fps=60,
           hue=h='180+60*sin(2*PI*t/4.6692)':s=2.5,
           gblur=sigma=0.15:steps=1[bg_mandelbrot];

      [2:v]scale=1920:1080,
           colorchannelmixer=aa=0.40,
           rotate=t*2*PI/10:c=black@0:ow=1920:oh=1080,
           sendcmd=f=$TMP_SAF_ANALYSE/snap_mod.txt,
           hue=h='160+(30*val)':s=2.5+(1.0*val)[omakoma_layer];

      [bg_combined][wif_panel]overlay=35:35:shortest=1[v1];
      [bg_mandelbrot][omakoma_layer]overlay=0:0:shortest=1[bg_combined];

      [a_wif]lowpass=f=200,showfreqs=s=280x110:mode=bar:cmode=separate:colors=red|orange[wif_s];
      [wif_s]drawbox=x=0:y=0:w=iw:h=ih:color=0xff4500@0.85:t=2[wif_panel];

      [a_mif]bandpass=f=1000:width_type=h:w=800,showfreqs=s=280x110:mode=bar:cmode=separate:colors=yellow|green[mif_s];
      [mif_s]drawbox=x=0:y=0:w=iw:h=ih:color=0x32cd32@0.85:t=2[mif_panel];

      [a_hif]highpass=f=3000,showfreqs=s=280x110:mode=bar:cmode=separate:colors=cyan|blue[hif_s];
      [hif_s]drawbox=x=0:y=0:w=iw:h=ih:color=0x00ffff@0.85:t=2[hif_panel];

      [a_phase]showwaves=s=1800x90:mode=line:colors=0x00ffff@0.95|0xff00ff@0.95|0xffff00@0.95[phase_s];
      [phase_s]drawbox=x=0:y=0:w=iw:h=ih:color=0xffffff@0.65:t=2[phase_panel];

      [bg_combined][wif_panel]overlay=35:35:shortest=1[v1];
      [v1][mif_panel]overlay=35:160:shortest=1[v2];
      [v2][hif_panel]overlay=35:285:shortest=1[v3];
      [v3][phase_panel]overlay=(W-w)/2:H-h-15:shortest=1[out]
    " \
    -map "[out]" -map "[a_out]" -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -c:a aac -b:a 256k -shortest "$OUTPUT_STREAM"
else
  ffmpeg -y -i "$TARGET_AUDIO" \
    -f lavfi -i "mandelbrot=s=1920x1080:maxiter=3320:start_x=-0.743643887037:start_y=0.131825904205" \
    -filter_complex "
      [0:a]asplit=5[a_wif][a_mif][a_hif][a_phase][a_out];

      [1:v]format=yuv420p,
           zoompan=z='1.002+0.0008*sin(2*PI*time/1.368)':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:s=1920x1080:fps=60,
           hue=h='180+60*sin(2*PI*t/4.6692)':s=2.5,
           gblur=sigma=0.15:steps=1[bg_mandelbrot];

      [a_wif]lowpass=f=200,showfreqs=s=280x110:mode=bar:cmode=separate:colors=red|orange[wif_s];
      [wif_s]drawbox=x=0:y=0:w=iw:h=ih:color=0xff4500@0.85:t=2[wif_panel];

      [a_mif]bandpass=f=1000:width_type=h:w=800,showfreqs=s=280x110:mode=bar:cmode=separate:colors=yellow|green[mif_s];
      [mif_s]drawbox=x=0:y=0:w=iw:h=ih:color=0x32cd32@0.85:t=2[mif_panel];

      [a_hif]highpass=f=3000,showfreqs=s=280x110:mode=bar:cmode=separate:colors=cyan|blue[hif_s];
      [hif_s]drawbox=x=0:y=0:w=iw:h=ih:color=0x00ffff@0.85:t=2[hif_panel];

      [a_phase]showwaves=s=1800x90:mode=line:colors=0x00ffff@0.95|0xff00ff@0.95|0xffff00@0.95[phase_s];
      [phase_s]drawbox=x=0:y=0:w=iw:h=ih:color=0xffffff@0.65:t=2[phase_panel];

      [bg_mandelbrot][wif_panel]overlay=35:35:shortest=1[v1];
      [v1][mif_panel]overlay=35:160:shortest=1[v2];
      [v2][hif_panel]overlay=35:285:shortest=1[v3];
      [v3][phase_panel]overlay=(W-w)/2:H-h-15:shortest=1[out]
    " \
    -map "[out]" -map "[a_out]" -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -c:a aac -b:a 256k -shortest "$OUTPUT_STREAM"
fi

rm -rf "$TMP_SAF_ANALYSE"
echo ""
echo "=== SAF V 33.2 RENDERING ERFOLGREICH! ==="
echo "Gespeichert unter: $OUTPUT_STREAM"
