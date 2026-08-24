#!/bin/bash
# SAF Audio Generator & Hybrid Visualizer Pipeline

AUDIO_INPUT="SAF_V29.3.5_Forward_Path_Master.wav"
BACKGROUND_IMG="saf_v29_visual.jpg"
OUTPUT_STREAM="saf_realtime_matrix.mp4"

echo "=== 1. Generiere SAF Audio Signal: $AUDIO_INPUT ==="

python3 -c "
import numpy as np
import scipy.io.wavfile as wav

sr = 44100
dur = 16.0
t = np.linspace(0, dur, int(sr * dur), False)

# SAF Parameter: N1=16, N2=257, 5pi Verschiebung
mod = (16 / 257) * (5 * np.pi)

# Sub-Bass Base (44 Hz) + Multi-Band Phase Shift (Traktor Deck-D Style)
f0 = 44.0
chs = []

for i in range(5):
    # Dynamischer 4-to-the-Floor Pulse (120 BPM)
    pulse = np.exp(-12.0 * ((t * 2.0) % 1.0))
    kick = np.sin(2 * np.pi * (f0 + 60.0 * pulse) * t) * pulse
    
    # 5D-Umfaltung Harmonics (Bifurkation Obertonkaskade)
    sweep_mod = np.sin(2 * np.pi * 0.1 * t + (i / 5.0) * 5 * np.pi * mod)
    high_overtones = sum([
        (0.2 / (h + 1)) * np.sin(2 * np.pi * (1760.0 * (h + 1) * (1 + 0.3 * sweep_mod)) * t)
        for h in range(4)
    ])
    
    # Sub-Drone + Modulationsschicht
    sub_drone = 0.4 * np.sin(2 * np.pi * f0 * (i + 1) * t)
    
    ch = (kick * 0.7 + sub_drone + high_overtones)
    chs.append(ch)

wave = np.vstack(chs).T
wave_norm = wave / np.max(np.abs(wave))
wave_int16 = np.int16(np.tanh(wave_norm * 1.3) / 1.3 * 32767)

wav.write('$AUDIO_INPUT', sr, wave_int16)
print('Audio-Synthese erfolgreich beendet.')
"

echo "=== 2. Prüfe Hintergrundbild ==="
if [ ! -f "$BACKGROUND_IMG" ]; then
    echo "Hintergrundbild $BACKGROUND_IMG nicht gefunden, generiere Platzhalter..."
    ffmpeg -y -f lavfi -i color=c=0x050a15:s=1920x1080 -vframes 1 "$BACKGROUND_IMG" >/dev/null 2>&1
fi

echo "=== 3. Starte SAF Audio-Visual Pipeline (Audio Fix & Smooth Wave) ==="

# Skaliert das Bild auf gerade Maße, zeichnet die durchgehende Cyan-Wellenform und encodiert Audio als AAC 320k
ffmpeg -y -i "$AUDIO_INPUT" -loop 1 -i "$BACKGROUND_IMG" \
  -filter_complex "[1:v]scale='trunc(iw/2)*2':'trunc(ih/2)*2'[bg];[0:a]showwaves=s=1716x624:mode=cline:colors=0x00ffff@0.85[wave];[bg][wave]overlay=(W-w)/2:(H-h)/2:shortest=1[out]" \
  -map "[out]" -map 0:a -c:v libx264 -preset fast -crf 18 -c:a aac -b:a 320k "$OUTPUT_STREAM"

echo "=== Render abgeschlossen: $OUTPUT_STREAM ==="
