#!/bin/bash
saf_start() {
    local hz=$(echo "scale=2; $1 / 60" | bc)
    python3 -c "import math, struct, wave; wav=wave.open('saf.wav','w'); wav.setnchannels(1); wav.setsampwidth(2); wav.setframerate(44100); [wav.writeframes(struct.pack('h', int(math.sin(2*3.1415*440*(i/44100)) * (0.6 + 0.4 * math.sin(2*3.1415*$hz*(i/44100)))))) for i in range(44100*10)]; wav.close()"
    
    # ffplay ist oft stabiler in Termux, da es nicht versucht, das Audio-Device exklusiv zu kapern
    ffplay -nodisp -loop 0 -autoexit -af "highpass=f=200,lowpass=f=4000" ~/saf.wav &
}
case "$1" in
    start) saf_start $2 ;;
    stop) pkill -9 ffplay ;;
    status) ps aux | grep ffplay | grep -v grep && echo "SAF läuft." || echo "SAF inaktiv." ;;
esac
