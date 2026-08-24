#!/bin/bash

# Zielsynthese-Ordner in SAF_Library erstellen
mkdir -p SAF_Library/01_Analog_Chaos_Tube_v44_v52
mkdir -p SAF_Library/01_Harmonic_Octaves_v56_v59
mkdir -p SAF_Library/02_Triplesplit_Core_v76_v83
mkdir -p SAF_Library/02_Hypercube_Mirrored_v84_v92

# Unsortierte Dateien aus LiDAR in die neuen SAF_Library-Ebenen verschieben
mv LiDAR/opt_saf_v4[4-9]*.wav LiDAR/opt_saf_v5[0-2]*.wav SAF_Library/01_Analog_Chaos_Tube_v44_v52/ 2>/dev/null
mv LiDAR/opt_saf_v5[6-9]*.wav LiDAR/opt_saf_v6[4-6]*.wav SAF_Library/01_Harmonic_Octaves_v56_v59/ 2>/dev/null
mv LiDAR/opt_saf_v7[6-9]*.wav LiDAR/opt_saf_v8[0-3]*.wav SAF_Library/02_Tripleslit_Core_v76_v83/ 2>/dev/null
mv LiDAR/opt_saf_v8[4-9]*.wav LiDAR/opt_saf_v9[0-2]*.wav SAF_Library/02_Hypercube_Mirrored_v84_v92/ 2>/dev/null

# Einzelne Hilfsdateien einsortieren
mkdir -p SAF_Library/00_Raw_Grooves_and_Scripts
mv LiDAR/generate_saf_v40_v43_lidar.py LiDAR/saf_spectral_groove_32beats.wav LiDAR/opt_spatial_sharpness_xpi.wav SAF_Library/00_Raw_Grooves_and_Scripts/ 2>/dev/null

echo "[SAF Cleanup Master] Sämtliche Alt-Bestände aus LiDAR vollständig in SAF_Library überführt!"
