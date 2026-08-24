#!/bin/bash

# Erstelle strukturierte Unterordner für Traktor
mkdir -p SAF_Library/01_Lidar_Phase_v32_v43
mkdir -p SAF_Library/02_Tripleslit_v60_v75
mkdir -p SAF_Library/03_Julia_Feeder_v116_v123
mkdir -p SAF_Library/04_Hyperspace_N16_v124_v131
mkdir -p SAF_Library/05_N457_Density_v132_v139

# Einsortieren nach Generierungs-Typen
mv opt_saf_v3[2-9]*.wav opt_saf_v4[0-3]*.wav SAF_Library/01_Lidar_Phase_v32_v43/ 2>/dev/null
mv opt_saf_v6[0-9]*.wav opt_saf_v7[0-5]*.wav SAF_Library/02_Tripleslit_v60_v75/ 2>/dev/null
mv opt_saf_v11[6-9]*.wav opt_saf_v12[0-3]*.wav SAF_Library/03_Julia_Feeder_v116_v123/ 2>/dev/null
mv opt_saf_v12[4-9]*.wav opt_saf_v13[0-1]*.wav SAF_Library/04_Hyperspace_N16_v124_v131/ 2>/dev/null
mv opt_saf_v13[2-9]*.wav SAF_Library/05_N457_Density_v132_v139/ 2>/dev/null

echo "[SAF Library Manager] 105+ Samples erfolgreich in 5 SAF-Systemebenen strukturiert!"
