# Wert zwischen 0.0 (Techno) und 1.0 (Ambient)
python3 -c "from saf_morph_synth import generate_morph_chaos; generate_morph_chaos('saf_morph.wav', morph=$1)"
cp saf_morph.wav /sdcard/Download/saf_morph_final.wav
echo "Regler auf $1 gesetzt. Datei liegt im Download-Ordner."
