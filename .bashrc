alias s='/data/data/com.termux/files/home/saf_live.sh start'
alias k='/data/data/com.termux/files/home/saf_live.sh stop'
alias p='/data/data/com.termux/files/home/saf_live.sh status'
alias saf-app='python ~/saf_sonification.py'

# SAF-Autostart-Logik
if [ -f ~/gesamt_saf.sh ]; then
    echo "--- SAF V29.3.3 AUTO-INITIALISIERUNG ---"
    bash ~/gesamt_saf.sh start &
fi
