#!/bin/bash
pkill -f python
# 1. Berechnung durchführen
python3 saf_v29_audio.py
# 2. Konvertierung mit korrekten Parametern für die Rohdaten
sox -r 44100 -b 16 -c 1 -e signed-integer -t raw saf_divergence.raw /sdcard/Download/saf_chaos_final.wav
echo "Audio erfolgreich unter /sdcard/Download/saf_chaos_final.wav gespeichert."
