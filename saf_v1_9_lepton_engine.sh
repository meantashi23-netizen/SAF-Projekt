#!/bin/bash
# SAF V1.9 Hybrid Lepton Engine (Optimierte Dateigröße / Visuell Verlustfrei)
set -e

SAF_DIR="$HOME/Desktop/5D-SAF Set/Video & π5"
mkdir -p "$SAF_DIR"

# 1. Dynamisches Schreiben des Python-Submoduls V29.3.5
cat << 'PYEOF' > saf_leptons.py
import numpy as np

class SAFLeptonData:
    ELEMENTARY_CHARGE_C = 1.602176634e-19
    PROTON_MASS_KG = 1.6726219e-27
    
    LEPTONS = {
        "elektron": {"symbol": "e-", "generation": 1, "charge_e": -1, "mass_MeV": 0.511, "mass_kg": 9.1093837015e-31, "lifetime_s": np.inf, "saf_freq_band": "WIF", "plasma_relevant": True},
        "elektron_neutrino": {"symbol": "nu_e", "generation": 1, "charge_e": 0, "mass_MeV": 8e-7, "mass_kg": 1.426e-36, "lifetime_s": np.inf, "saf_freq_band": "WIF", "plasma_relevant": False},
        "myon": {"symbol": "mu-", "generation": 2, "charge_e": -1, "mass_MeV": 105.66, "mass_kg": 1.883531627e-28, "lifetime_s": 2.1969811e-6, "saf_freq_band": "MIF", "plasma_relevant": False},
        "myon_neutrino": {"symbol": "nu_mu", "generation": 2, "charge_e": 0, "mass_MeV": 0.17, "mass_kg": 3.03e-31, "lifetime_s": np.inf, "saf_freq_band": "MIF", "plasma_relevant": False},
        "tauon": {"symbol": "tau-", "generation": 3, "charge_e": -1, "mass_MeV": 1776.86, "mass_kg": 3.16754e-27, "lifetime_s": 2.903e-13, "saf_freq_band": "HIF", "plasma_relevant": False},
        "tauon_neutrino": {"symbol": "nu_tau", "generation": 3, "charge_e": 0, "mass_MeV": 15.5, "mass_kg": 2.76e-29, "lifetime_s": np.inf, "saf_freq_band": "HIF", "plasma_relevant": False}
    }

    @classmethod
    def get_cyclotron_frequency(cls, particle_key: str, B_field_tesla: float) -> float:
        p = cls.LEPTONS.get(particle_key)
        if not p or p["charge_e"] == 0:
            return 0.0
        q = abs(p["charge_e"]) * cls.ELEMENTARY_CHARGE_C
        m = p["mass_kg"]
        return (q * B_field_tesla) / m

if __name__ == "__main__":
    omega_ce = SAFLeptonData.get_cyclotron_frequency("elektron", B_field_tesla=5.0)
    print(f"{omega_ce:.4e}")
PYEOF

# 2. Plasma-Resonanz berechnen
echo "=== SAF V1.9 Berechne Tokamak Plasma-Resonanz (5 Tesla) ==="
OMEGA_CE=$(python3 saf_leptons.py)
echo "Elektronen-Zyklozyklotronfrequenz (omega_ce): $OMEGA_CE rad/s"

# 3. Sichere Pfadsuche via Python
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
    echo "FEHLER: Datei konnte via Python FS-Walker nicht gefunden werden."
    exit 1
fi

echo "=== Exakte Audioquelle geladen: $TARGET_AUDIO ==="

OUTPUT_STREAM="$SAF_DIR/saf_v1_9_lepton_matrix_techno.mp4"

# 4. Rendering via FFmpeg (CRF 19 für optimale Kompression ohne Qualitätsverlust)
echo "=== SAF V1.9 Multi-Layer Pipeline gestartet ==="
ffmpeg -y -i "$TARGET_AUDIO" -f lavfi -i "mandelbrot=s=1920x1080:maxiter=2500:start_x=-0.743643887037:start_y=0.131825904205" \
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
    [wif_panel]drawbox=x=0:y=0:w=iw:h=ih:color=0xff4500@0.8:t=3[wif_frame];

    [a_mif]bandpass=f=1000:width_type=h:w=800,showfreqs=s=300x120:mode=bar:cmode=separate:colors=yellow|green[mif_panel];
    [mif_panel]drawbox=x=0:y=0:w=iw:h=ih:color=0x32cd32@0.8:t=3[mif_frame];

    [a_hif]highpass=f=3000,showfreqs=s=300x120:mode=bar:cmode=separate:colors=cyan|blue[hif_panel];
    [hif_panel]drawbox=x=0:y=0:w=iw:h=ih:color=0x00ffff@0.8:t=3[hif_frame];

    [a_phase]showwaves=s=1800x120:mode=line:colors=0x00ffff@0.9|0xff00ff@0.9|0xffff00@0.9[phase_stream];
    [phase_stream]drawbox=x=0:y=0:w=iw:h=ih:color=0xffffff@0.6:t=2[phase_panel];

    [bg_flower_mesh][wif_frame]overlay=30:30:shortest=1[v_stage1];
    [v_stage1][mif_frame]overlay=30:160:shortest=1[v_stage2];
    [v_stage2][hif_frame]overlay=30:290:shortest=1[v_stage3];
    [v_stage3][phase_panel]overlay=(W-w)/2:H-h-20:shortest=1[out]
  " \
  -map "[out]" -map "[a_out]" -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -c:a aac -b:a 256k "$OUTPUT_STREAM"

echo "=== SAF V1.9 Engine Rendering abgeschlossen! Output: $OUTPUT_STREAM ==="
