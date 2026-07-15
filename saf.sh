#!/bin/bash
# Zuerst Generator ausführen
python3 ~/gen.py
# Dann Player ohne jegliche Filter starten
mpv --no-video --loop=inf ~/saf.wav
