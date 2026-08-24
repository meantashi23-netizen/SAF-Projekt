#!/bin/bash

# 1. Erstelle den fehlenden N1080 Ordner und verschiebe v140-v147 hinein
mkdir -p SAF_Library/06_N1080_Fibonacci_v140_v147
mv SAF_Library/opt_saf_v14[0-7]*.wav SAF_Library/06_N1080_Fibonacci_v140_v147/ 2>/dev/null

# 2. Weitere Ordner für die losen v93 - v115 Dateien anlegen
mkdir -p SAF_Library/00_Mandelbrot_Inversion_v93_v99
mkdir -p SAF_Library/00_Apex_Matrix_v100_v107
mkdir -p SAF_Library/00_5D_Julia_Apex_v108_v115

# 3. Lose LiDAR-Dateien einsortieren
mv opt_saf_v9[3-9]*.wav LiDAR/opt_saf_v9[3-9]*.wav SAF_Library/00_Mandelbrot_Inversion_v93_v99/ 2>/dev/null
mv opt_saf_v10[0-7]*.wav LiDAR/opt_saf_v10[0-7]*.wav SAF_Library/00_Apex_Matrix_v100_v107/ 2>/dev/null
mv opt_saf_v10[8-9]*.wav opt_saf_v11[0-5]*.wav LiDAR/opt_saf_v10[8-9]*.wav LiDAR/opt_saf_v11[0-5]*.wav SAF_Library/00_5D_Julia_Apex_v108_v115/ 2>/dev/null

echo "[SAF Fix] Alle N=1080 und LiDAR-Reste perfekt in SAF_Library aufgeräumt!"
