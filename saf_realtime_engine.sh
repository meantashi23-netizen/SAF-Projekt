#!/bin/bash
# SAF Hybrid Visualizer: Audio Encoding Fix + Connected Waveform

AUDIO_INPUT="SAF_V29.3.5_Forward_Path_Master.wav"
BACKGROUND_IMG="saf_v29_visual.jpg"
OUTPUT_STREAM="saf_realtime_matrix.mp4"

echo "=== Starte SAF Audio-Visual Pipeline (Audio Fix & Smooth Wave) ==="

# Skaliert das Bild sauber auf gerade Maße, zeichnet durchgehende Wellenform und encodiert Audio als AAC 320k
ffmpeg -y -i "$AUDIO_INPUT" -loop 1 -i "$BACKGROUND_IMG" \
  -filter_complex "[1:v]scale='trunc(iw/2)*2':'trunc(ih/2)*2'[bg];[0:a]showwaves=s=1716x624:mode=cline:colors=0x00ffff@0.85[wave];[bg][wave]overlay=0:0:shortest=1[out]" \
  -map "[out]" -map 0:a -c:v libx264 -preset fast -crf 18 -c:a aac -b:a 320k "$OUTPUT_STREAM"

echo "Render abgeschlossen: $OUTPUT_STREAM"
