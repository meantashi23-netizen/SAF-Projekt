#!/bin/bash
echo "Starte SAF-Daten..."
python3 saf_calc.py
python3 auto_bifurcation.py
python3 analyze_saf.py
git add .
git commit -m "SAF Update"
git push
echo "Fertig."
