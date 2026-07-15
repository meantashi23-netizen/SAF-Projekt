#!/bin/bash
pkill -f python
pkill -f play # Beende auch den Audio-Prozess
rm -f saf_data/saf_log.txt
nohup python3 saf_audio_synth.py > /dev/null 2>&1 &
python3 auto_bifurcation_audio.py
pkill -f python
pkill -f play # Finaler Stop
