#!/bin/bash
# Gesamt-Sync für SAF-Projekt

echo "--- SAF V29.3.3 SYNC START ---"
cd ~/SAF-Projekt

# 1. Sicherstellen, dass Git bereit ist
git init 2>/dev/null

# 2. Remote-Verbindung setzen
git remote add origin git@github.com:meantashi23-netizen/SAF-Projekt.git 2>/dev/null || git remote set-url origin git@github.com:meantashi23-netizen/SAF-Projekt.git

# 3. Dateien zum Staging hinzufügen
# Hinweis: Das ignoriert automatisch alles, was in .gitignore steht!
git add .

# 4. Commit mit Zeitstempel
git commit -m "Auto-Sync: $(date)" || echo "Nichts neues zum Committen."

# 5. Push in die Cloud
git push -u origin main

echo "--- SAF SYNC ABGESCHLOSSEN ---"
