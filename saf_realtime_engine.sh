#!/bin/bash
# SAF Hybrid Visualizer: J(o)=1.39 Image + Waveform Overlay

AUDIO_INPUT="SAF_V29.3.5_Forward_Path_Master.wav"
BACKGROUND_IMG="saf_v29_visual.jpg"
OUTPUT_STREAM="saf_realtime_matrix.mp4"

echo "=== Starte SAF Hybrid Audio-Visual Pipeline ==="

# Generiert die Waveform mit transparentem Hintergrund und blendet sie über das Visual
ffmpeg -y -i "$AUDIO_INPUT" -loop 1 -i "$BACKGROUND_IMG" \
  -filter_complex "[0:a]showwaves=s=1920x1080:mode=line:colors=0x00ffff@0.85[wave];[1:v][wave]overlay=0:0:shortest=1[out]" \
  -map "[out]" -map 0:a -c:v libx264 -preset fast -crf 18 -c:a copy "$OUTPUT_STREAM"

echo "Hybrid Render abgeschlossen: $OUTPUT_STREAM"
