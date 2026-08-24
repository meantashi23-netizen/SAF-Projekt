#!/bin/bash
# SAF 5D-Engine - G-Hutabaci Warp V1.8 & 5-Kanal Spektralkopplung

SAF_DIR="$HOME/Desktop/5D-SAF Set/Video & π5"
AUDIO_NAME="Recording_2026-07-30_01h50m56s.wav"

if [ -f "$SAF_DIR/$AUDIO_NAME" ]; then
    AUDIO_INPUT="$SAF_DIR/$AUDIO_NAME"
elif [ -d "$SAF_DIR" ]; then
    AUDIO_INPUT=$(ls -t "$SAF_DIR"/*.wav 2>/dev/null | head -n 1)
fi

OUTPUT_STREAM="$SAF_DIR/saf_5d_hutabaci_warp_v1.8.mp4"

if [ -z "$AUDIO_INPUT" ] || [ ! -f "$AUDIO_INPUT" ]; then
    echo "Fehler: Keine .wav Audioquelle gefunden!"
    exit 1
fi

echo "=== SAF 5D G-Hutabaci Warp V1.8 Pipeline gestartet ==="

# 1. 5D Audio-Split in 5 Spektralbänder (Bass, Low-Mid, Mid, High-Mid, High)
# 2. G-Hutabaci Warp via lenscorrection (Hyper-Dimensionale Krümmung)
# 3. Jitter-Free 60 FPS Zoom mit maxiter=1200 für tiefste Bifurkations-Filamente
ffmpeg -y -i "$AUDIO_INPUT" -f lavfi -i "mandelbrot=s=1920x1080:maxiter=1200:start_x=-0.743643887037:start_y=0.131825904205" \
  -filter_complex "
    [0:a]asetrate=44100*0.333333333333,aresample=44100,asplit=5[a_sub][a_lowmid][a_mid][a_highmid][a_out];
    
    [1:v]format=yuv420p,
         zoompan=z='1.0005+0.0009*on':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:s=1920x1080:fps=60,
         lenscorrection=cx=0.5:cy=0.5:k1=-0.18:k2=0.06,
         hue=h='140+35*sin(t*0.4)':s=2.2,
         perspective=x0=W*0.06:y0=H*0.08:x1=W*0.94:y1=H*0.03:x2=W*0.04:y2=H*0.96:x3=W*0.96:y3=H*0.91:interpolation=1[bg_5d_hutabaci];
    
    [a_sub]lowpass=f=100,showwaves=s=1200x400:mode=cline:colors=0xff0055@0.90[wave_1_sub];
    [a_lowmid]bandpass=f=400:width_type=h:w=500,showwaves=s=1200x400:mode=cline:colors=0x00ffff@0.80[wave_2_lm];
    [a_mid]bandpass=f=1500:width_type=h:w=1500,showwaves=s=1200x400:mode=cline:colors=0x00ff55@0.80[wave_3_mid];
    [a_highmid]bandpass=f=4500:width_type=h:w=2500,showwaves=s=1200x400:mode=cline:colors=0xff00cc@0.80[wave_4_hm];

    [wave_2_lm]rotate=-45*PI/180:ow=hypot(iw\,ih):oh=ow:c=none[slit_left];
    [wave_3_mid]rotate=45*PI/180:ow=hypot(iw\,ih):oh=ow:c=none[slit_right];
    [wave_4_hm]rotate=90*PI/180:ow=hypot(iw\,ih):oh=ow:c=none[slit_vertical];

    [bg_5d_hutabaci][slit_left]overlay=(W-w)/2-350:(H-h)/2:shortest=1[v1];
    [v1][slit_right]overlay=(W-w)/2+350:(H-h)/2:shortest=1[v2];
    [v2][slit_vertical]overlay=(W-w)/2:(H-h)/2:shortest=1[v3];
    [v3][wave_1_sub]overlay=(W-w)/2:(H-h)/2:shortest=1[out]
  " \
  -map "[out]" -map "[a_out]" -c:v libx264 -preset slow -crf 14 -pix_fmt yuv420p -c:a aac -b:a 320k "$OUTPUT_STREAM"

echo "=== 5D G-Hutabaci Warp Rendering erfolgreich abgeschlossen! Output: $OUTPUT_STREAM ==="
