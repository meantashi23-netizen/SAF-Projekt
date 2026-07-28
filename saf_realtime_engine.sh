#!/bin/bash
# SAF Realtime Audio-Visual Coupling Engine

AUDIO_INPUT="SAF_V29.3.5_Forward_Path_Master.wav"
OUTPUT_STREAM="saf_realtime_matrix.mp4"

echo "=== Starte SAF Realtime Audio-Visual Pipeline ==="

ffmpeg -y -i "$AUDIO_INPUT" \
  -filter_complex "[0:a]avectorscope=s=1920x1080:m=lissajous:rc=0:gc=255:bc=200:zoom=1.5[out]" \
  -map "[out]" -map 0:a -c:v libx264 -preset fast -crf 18 -c:a copy "$OUTPUT_STREAM"

echo "Realtime Coupling Video abgeschlossen: $OUTPUT_STREAM"
