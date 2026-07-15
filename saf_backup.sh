#!/bin/bash

# Pfad zu deinem Repository
cd /data/data/com.termux/files/home/SAF-Projekt

echo "Starte Auto-Backup-Schleife..."

while true; do
    echo "Prüfe auf Änderungen..."
    git add .
    # Der Befehl commit mit "|| true" verhindert, dass das Skript abbricht, wenn es nichts zu committen gibt
    git commit -m "Auto-Backup $(date)" || true
    git push origin main
    
    echo "Backup abgeschlossen. Warte 1 Stunde..."
    sleep 3600  # 3600 Sekunden = 1 Stunde
done

