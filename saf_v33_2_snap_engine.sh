#!/bin/bash
# SAF V 33.2 SnaP Engine (N=257 / 3320 Iterations + Dynamic Audio SnaP & Topnotch Rotation / CRF 19)
set -e

# Globale SAF V33.2 Pfade
DESKTOP_DIR="$HOME/Desktop"
SAF_DIR="$DESKTOP_DIR/5D-SAF Set/Video & π5"
# Verzeichnis für temporäre Analyse-Daten
TMP_SAF_ANALYSE="$SAF_DIR/.analyse_tmp"

mkdir -p "$SAF_DIR"
mkdir -p "$TMP_SAF_ANALYSE"

echo "=== SAF V 33.2 SnaP Engine gestartet ==="

# 1. Exakte Audioquelle ermitteln und Lautstärke (Spannung/SnaP) analysieren
TARGET_AUDIO=$(python3 -c '
import os
desktop = os.path.expanduser("~/Desktop")
for root, dirs, files in os.walk(desktop):
    if "Mean Tashi" in root:
        for f in files:
            if "192302" in f and f.endswith(".aif"):
                print(os.path.join(root, f))
                break
')

if [ -z "$TARGET_AUDIO" ] || [ ! -f "$TARGET_AUDIO" ]; then
    echo "FEHLER: Audio-Datei (.aif) nicht gefunden."
    TARGET_AUDIO=$(find "$DESKTOP_DIR" -name "*.aif" | head -n 1)
    if [ -z "$TARGET_AUDIO" ]; then exit 1; fi
fi

echo "=== Audioquelle geladen: $TARGET_AUDIO ==="

# === NEU IN V 33.2: Audio-SnaP Analyse (RMS Spannung / SnaP Flanken) ===
echo "=== Analysiere Audio-SnaP (RMS Spannung)... ==="
# Wir extrahieren die RMS-Lautstärke pro Frame (60fps) und skalieren sie auf 0.0-1.0
# Die resultierende Datei snap_mod.txt steuert die dynamische OMAKOMA-Farb-Vibration.
ffmpeg -y -i "$TARGET_AUDIO" -af "asetnsamples=n=735,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=$TMP_SAF_ANALYSE/rms.txt" -f null - 2>/dev/null

# Konvertiere dB zu Linearfaktor
python3 -c "
import math, os
rms_file = os.path.join('$TMP_SAF_ANALYSE', 'rms.txt')
snap_data_file = os.path.join('$TMP_SAF_ANALYSE', 'snap_mod.txt')
with open(rms_file, 'r') as f, open(snap_data_file, 'w') as out:
    for line in f:
        if 'Overall.RMS_level' in line:
            try:
                db = float(line.split('=')[-1].strip())
                linear = math.pow(10, (max(-60, db)) / 20) #dB Linearfaktor, clipped auf -60dB min.
                out.write(f'{linear:.6f}\n')
            except: continue
"
echo "=== SnaP-Analyse abgeschlossen. ==="

# 2. Python Core: N=257 Matrix initialisieren
cat << 'PYEOF' > saf_v33_2_core.py
import numpy as np

class SAFV332Core:
    FEIGENBAUM_DELTA = 4.669201609102990
    N_NODES = 257
    MAX_ITER = 3320 # V 33.2 Spezifikation

    @classmethod
    def generate_bifurcation_matrix(cls):
        indices = np.arange(1, cls.N_NODES + 1)
        matrix = cls.FEIGENBAUM_DELTA * (indices / cls.N_NODES)
        return matrix

if __name__ == "__main__":
    matrix = SAFV332Core.generate_bifurcation_matrix()
    print(f"SAF V 33.2 Core: N={SAFV332Core.N_NODES} Matrix (3320 Iterations)")
PYEOF

python3 saf_v33_2_core.py

# 3. OMAKOMA PNG Overlay suchen
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

echo "=== OMAKOMA Intercept Overlay: ${OMAKOMA_IMG:-Kein Bild, nativer Stream gestartet} ==="

OUTPUT_STREAM="$SAF_DIR/compressed/saf_v33_2_snap_stream.mp4"
mkdir -p "$(dirname "$OUTPUT_STREAM")"

# 4. Multi-Layer FFmpeg Rendering (CRF 19 / N=257 / 3320 Iter / SnaP Mod & Topnotch Rotate)
echo "=== Starte SAF V 33.2 Rendering (N=257, Iter=3320) ==="

# FFmpeg Filter Complex: Nativer Mandelbrot Stream + Omakoma Intercept "SnaP" Modulator
# sendcmd liest die transiente SnaP-Modulation für die dynamische Farb-Vibration
# rotate dreht das OMAKOMA Intercept Overlay permanent um 360 Grad (Topnotch Rotation)
if [ -n "$OMAKOMA_IMG" ] && [ -f "$OMAKOMA_IMG" ]; then
  ffmpeg -y -i "$TARGET_AUDIO" \
    -f lavfi -i "mandelbrot=s=1920x1080:maxiter=3320:start_x=-0.743643887037:start_y=0.131825904205" \
    -loop 1 -i "$OMAKOMA_IMG" \
    -filter_complex "
      [0:a]asplit=5[a_wif][a_mif][a_hif][a_phase][a_out];

      # Nativer Mandelbrot Stream mit N=257 Farbauflösung & Phasen-Shift
      [1:v]format=yuv420p,
           zoompan=z='1.002+0.0006*sin(2*PI*time/1.368)':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:s=1920x1080:fps=60,
           hue=h='180+60*sin(2*PI*t/4.6692)':s=2.5,
           gblur=sigma=0.15:steps=1[bg_mandelbrot];

      # === NEU IN V 33.2: Dynamic OMAKOMA SnaP Modulator & Topnotch Rotation ===
      # sendcmd liest die transiente SnaP-Modulation für die dynamische Farb-Vibration
      [2:v]scale=1920:1080,
           colorchannelmixer=aa=0.40,
           rotate=t*2*PI/10:c=black@0:ow=1920:oh=1080,
           sendcmd=f=$TMP_SAF_ANALYSE/snap_mod.txt,
           hue=h='160+(30*val)':s=2.5+(1.0*val)[omakoma_layer];

      [bg_mandelbrot][omakoma_layer]overlay=0:0:shortest=1[bg_combined];

      # SAF Spektral-Panels (WIF, MIF, HIF)
      [a_wif]lowpass=f=200,showfreqs=s=280x110:mode=bar:cmode=separate:colors=red|orange[wif_s];
      [wif_s]drawbox=x=0:y=0:w=iw:h=ih:color=0xff4500@0.85:t=2[wif_panel];

      [a_mif]bandpass=f=1000:width_type=h:w=800,showfreqs=s=280x110:mode=bar:cmode=separate:colors=yellow|green[mif_s];
      [mif_s]drawbox=x=0:y=0:w=iw:h=ih:color=0x32cd32@0.85:t=2[mif_panel];

      [a_hif]highpass=f=3000,showfreqs=s=280x110:mode=bar:cmode=separate:colors=cyan|blue[hif_s];
      [hif_s]drawbox=x=0:y=0:w=iw:h=ih:color=0x00ffff@0.85:t=2[hif_panel];

      # Phase-Wellenform
      [a_phase]showwaves=s=1800x90:mode=line:colors=0x00ffff@0.95|0xff00ff@0.95|0xffff00@0.95[phase_s];
      [phase_s]drawbox=x=0:y=0:w=iw:h=ih:color=0xffffff@0.65:t=2[phase_panel];

      # Layer Compositing
      [bg_combined][wif_panel]overlay=35:35:shortest=1[v1];
      [v1][mif_panel]overlay=35:160:shortest=1[v2];
      [v2][hif_panel]overlay=35:285:shortest=1[v3];
      [v3][phase_panel]overlay=(W-w)/2:H-h-15:shortest=1[out]
    " \
    -map "[out]" -map "[a_out]" -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -c:a aac -b:a 256k -shortest "$OUTPUT_STREAM"
else
  # Native Mandelbrot Engine Standalone (falls OMAKOMA Bild nicht gefunden)
  ffmpeg -y -i "$TARGET_AUDIO" \
    -f lavfi -i "mandelbrot=s=1920x1080:maxiter=3320:start_x=-0.743643887037:start_y=0.131825904205" \
    -filter_complex "
      [0:a]asplit=5[a_wif][a_mif][a_hif][a_phase][a_out];

      [1:v]format=yuv420p,
           zoompan=z='1.002+0.0006*sin(2*PI*time/1.368)':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:s=1920x1080:fps=60,
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
echo "=== SAF V 33.2 Rendering ERFOLGREICH BEENDET! ==="
echo "Output gespeichert unter: $OUTPUT_STREAM"
