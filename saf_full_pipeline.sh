#!/usr/bin/env bash

echo "=== [1/4] Erstelle SAF V41.0 Vector Engine & Video Renderer ==="
cat << 'PYEOF' > render_mp4.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

class SAF41Render:
    def __init__(self, n_stages=200):
        self.n = n_stages
        self.feigenbaum = np.array([0.987, 0.933, 0.937, 0.954])

    def mesh(self, t):
        u = np.linspace(0, 2*np.pi, self.n)
        v = np.linspace(-np.pi/2, np.pi/2, self.n)
        U, V = np.meshgrid(u, v)
        w = np.sin(U * self.feigenbaum[0] + t) * np.cos(V * self.feigenbaum[1] + np.pi/2)
        X = (1 + 0.5 * np.cos(V + w)) * np.cos(U)
        Y = (1 + 0.5 * np.cos(V + w)) * np.sin(U)
        Z = 0.5 * np.sin(V + w) + 0.2 * np.sin(self.feigenbaum[2] * U * t)
        return X, Y, Z

r = SAF41Render()
fig = plt.figure(figsize=(10, 8), dpi=100)
ax = fig.add_subplot(111, projection="3d")

writer = FFMpegWriter(fps=30, metadata=dict(artist='SAF Engine'), bitrate=1800)

with writer.saving(fig, "saf_v41_render.mp4", 100):
    for i in range(150):
        ax.clear()
        t = i * 0.04
        X, Y, Z = r.mesh(t)
        ax.plot_surface(X, Y, Z, cmap="magma", edgecolor="none", alpha=0.9)
        ax.set_title(f"SAF V41.0 Engine Frame {i:03d}")
        ax.view_init(elev=20 + np.sin(t)*10, azim=i*2)
        writer.grab_frame()
PYEOF

echo "=== [2/4] Erstelle SAF V41.0 Audio-Synthese Engine ==="
cat << 'PYEOF' > saf_audio_synth.py
import numpy as np
import wave
import struct

class SAF41AudioEngine:
    def __init__(self, bpm=87.273, sample_rate=44100):
        self.bpm = bpm
        self.sr = sample_rate
        self.feigenbaum = np.array([0.987, 0.933, 0.937, 0.954])
        self.phase_shift = np.pi / 2.0
        self.seconds_per_bar = (60.0 / self.bpm) * 4.0
        self.duration = self.seconds_per_bar * 8.0 
        self.num_samples = int(self.sr * self.duration)

    def generate_stems(self):
        t_vec = np.linspace(0, self.duration, self.num_samples, endpoint=False)
        f_sub = 87.273 / 2.0  
        f_mid = f_sub * 3.0   
        f_high = f_sub * 8.0  

        z_mod = np.sin(2 * np.pi * f_sub * t_vec + self.phase_shift * np.cos(t_vec * 0.5))
        stem_sub = 0.7 * np.tanh(z_mod * 1.5)

        fm_mod = np.sin(2 * np.pi * (f_mid * self.feigenbaum[0]) * t_vec + 
                        np.sin(2 * np.pi * (f_mid * self.feigenbaum[1]) * t_vec))
        stem_mid = 0.5 * fm_mod * (0.8 + 0.2 * np.sin(2 * np.pi * (self.bpm / 60.0) * t_vec))

        phase_sweep = np.sin(2 * np.pi * f_high * t_vec + self.feigenbaum[2] * np.sin(t_vec * 2.0))
        stem_high = 0.3 * phase_sweep * np.cos(np.pi * t_vec / self.seconds_per_bar)

        return stem_sub, stem_mid, stem_high

    def save_wav(self, filename, audio_data):
        max_val = np.max(np.abs(audio_data))
        if max_val > 0:
            audio_data = audio_data / max_val * 0.95

        packed_data = bytearray()
        for s in audio_data:
            val = int(s * 32767)
            packed_data.extend(struct.pack('<h', val))

        with wave.open(filename, 'w') as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(self.sr)
            f.writeframes(packed_data)

if __name__ == "__main__":
    synth = SAF41AudioEngine(bpm=87.273)
    sub, mid, high = synth.generate_stems()
    synth.save_wav("saf_stem1_sub_87.273bpm.wav", sub)
    synth.save_wav("saf_stem2_mid_87.273bpm.wav", mid)
    synth.save_wav("saf_stem3_high_87.273bpm.wav", high)
    master = (sub * 0.5) + (mid * 0.3) + (high * 0.2)
    synth.save_wav("saf_master_mix_87.273bpm.wav", master)
PYEOF

echo "=== [3/4] Führe Rendering & Audio-Synthese aus ==="
python3 saf_audio_synth.py
python3 render_mp4.py

echo "=== [4/4] Automatischer Git-Sync & Cleanup ==="
find . -name ".DS_Store" -delete
echo ".DS_Store" >> .gitignore
git add .
git commit -m "feat(saf41): auto-render mp4 video, audio stems and clean repository" 2>/dev/null
git remote set-url origin git@github.com:meantashi23-netizen/SAF-Projekt.git
git push origin main

echo "=== SAF V41.0 Gesamtausführung erfolgreich beendet! ==="
