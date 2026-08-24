#!/bin/bash

# SAF (Spatial Audio Fusion) - TERMINAL SYNTHESE-EINHEIT
GREEN='\033[0;32m'
GOLD='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GOLD}===================================================================="
echo -e "       SAF (Spatial Audio Fusion) - TERMINAL SYNTHESE-EINHEIT"
echo -e "====================================================================${NC}"

OUTPUT_FILE="opt_spatial_sharpness_xpi.wav"
TEMP_FILE="temp_saf.wav"
SAMPLE_RATE=44100
DURATION_SEC=10
BASE_FREQ=261.63 # C4
PI="3.141592653589793"
X_PI_KOEFF="196.8334523"

echo -e "\n${BLUE}[SAF-BERECHNUNG]${NC} Starte Quantisierungs-Berechnung..."
QUANT_1_8_Hertz=$(echo "scale=5; 120 / 60 * 2" | bc)
QUANT_5_6_Hertz=$(echo "scale=5; (120 / 60) * (6 / 5)" | bc)
SAF_FUSION_FREQ=$(echo "scale=5; ${QUANT_1_8_Hertz} + ${QUANT_5_6_Hertz}" | bc)

echo -e "  > 1/8 Zählzeit: ${GREEN}${QUANT_1_8_Hertz} Hz${NC}"
echo -e "  > 5/6 Zählzeit: ${GREEN}${QUANT_5_6_Hertz} Hz${NC}"
echo -e "  > ${GOLD}SAF FUSION-FREQUENZ: ${SAF_FUSION_FREQ} Hz${NC}"

X_PI_DENSITY=$(echo "scale=10; ${X_PI_KOEFF} * ${PI}" | bc)
echo -e "  > ${GOLD}BERECHNETE xπ-PHASEN-DICHTE: ${X_PI_DENSITY} Hz${NC}"

CHAOS_FREQ=$(echo "scale=2; ${BASE_FREQ} / 16" | bc)

echo -e "\n${GREEN}[AUSFÜHRUNG]${NC} Führe SoX-Synthese aus..."

# Step 1: Grundwelle (C4 Stereo mit Phasenverschiebung)
sox -n -r ${SAMPLE_RATE} -c 2 ${TEMP_FILE} synth ${DURATION_SEC} sine ${BASE_FREQ} sine ${BASE_FREQ} 0 25

# Step 2: Amplitudenmodulation mit Chaos-Frequenz (N=16) & Quantisierungs-Quadratwelle
sox ${TEMP_FILE} ${OUTPUT_FILE} synth ${DURATION_SEC} amsine ${CHAOS_FREQ} amsine ${X_PI_DENSITY} gain -n -3

# Aufräumen
rm -f ${TEMP_FILE}

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}===================================================================="
    echo -e "       SAF-SYNTHESE ERFOLGREICH ABGESCHLOSSEN"
    echo -e "====================================================================${NC}"
    echo -e "Datei ${GOLD}${OUTPUT_FILE}${NC} wurde generiert."
else
    echo -e "\n${RED}===================================================================="
    echo -e "       FEHLER BEI DER SAF-SYNTHESE"
    echo -e "====================================================================${NC}"
fi
