#!/usr/bin/env bash

set -e

echo "=== [1/4] Erstelle Audio-Synthese Engine (87.273 BPM) ==="
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
    print("Audio Stems erfolgreich generiert.")
PYEOF

echo "=== [2/4] Erstelle Audio-Reaktive Vektor Render Engine ==="
cat << 'PYEOF' > render_reaktiv.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter
import wave
import struct

def get_stem_amplitudes(wav_file, num_frames=150):
    try:
        with wave.open(wav_file, 'rb') as w:
            sr = w.getframerate()
            num_samples = w.getnframes()
            audio_data = w.readframes(num_samples)
            audio_array = np.array(struct.unpack(f'<{num_samples}h', audio_data), dtype=np.float32)
            audio_array /= 32768.0
            
            samples_per_frame = int(sr / 30.0)
            amplitudes = []
            for i in range(num_frames):
                start = i * samples_per_frame
                end = start + samples_per_frame
                if start >= num_samples:
                    amplitudes.append(0.0)
                    continue
                if end > num_samples:
                    end = num_samples
                chunk = audio_array[start:end]
                rms = np.sqrt(np.mean(chunk**2)) if len(chunk) > 0 else 0.0
                amplitudes.append(rms)
            return np.array(amplitudes)
    except FileNotFoundError:
        print(f"Warnung: {wav_file} nicht gefunden. Nutze Fallback-Amplituden.")
        return np.zeros(num_frames)

class SAF41AudioReactiveRender:
    def __init__(self, n_stages=100, num_frames=150):
        self.n = n_stages
        self.feigenbaum = np.array([0.987, 0.933, 0.937, 0.954])
        self.num_frames = num_frames
        
        self.amp_sub = get_stem_amplitudes("saf_stem1_sub_87.273bpm.wav", num_frames)
        self.amp_mid = get_stem_amplitudes("saf_stem2_mid_87.273bpm.wav", num_frames)
        self.amp_high = get_stem_amplitudes("saf_stem3_high_87.273bpm.wav", num_frames)
        
        max_sub = np.max(self.amp_sub) + 1e-6
        max_mid = np.max(self.amp_mid) + 1e-6
        max_high = np.max(self.amp_high) + 1e-6
        
        self.amp_sub = (self.amp_sub / max_sub) * 2.0
        self.amp_mid = (self.amp_mid / max_mid) * 1.0
        self.amp_high = (self.amp_high / max_high) * 0.5

    def mesh(self, i):
        t = i * 0.04
        u = np.linspace(0, 2*np.pi, self.n)
        v = np.linspace(-np.pi/2, np.pi/2, self.n)
        U, V = np.meshgrid(u, v)
        
        a_s = self.amp_sub[i]
        a_m = self.amp_mid[i]
        a_h = self.amp_high[i]
        
        base_radius = 1.0 + (a_s * 0.3)
        w_mid = np.sin(U * (self.feigenbaum[0] + a_m*0.1) + t) * \
                np.cos(V * (self.feigenbaum[1] + a_m*0.05) + np.pi/2)
        z_high = (a_h * 0.1) * np.sin(self.feigenbaum[2] * U * 20.0 + t*10.0)
        
        X = (base_radius + 0.5 * np.cos(V + w_mid)) * np.cos(U)
        Y = (base_radius + 0.5 * np.cos(V + w_mid)) * np.sin(U)
        Z = 0.5 * np.sin(V + w_mid) + 0.2 * np.sin(self.feigenbaum[2] * U * t) + z_high
        
        return X, Y, Z

print("Analysiere Audio-Stems und starte audio-reaktives Rendering...")
r = SAF41AudioReactiveRender(n_stages=100, num_frames=150)
fig = plt.figure(figsize=(10, 8), dpi=100, facecolor='black')
ax = fig.add_subplot(111, projection="3d", facecolor='black')
ax.set_axis_off()

writer = FFMpegWriter(fps=30, metadata=dict(artist='SAF Audio-Reactive Engine'), bitrate=4000)

with writer.saving(fig, "saf_v41_REAKTIVE.mp4", 100):
    for i in range(150):
        ax.clear()
        ax.set_axis_off()
        ax.set_xlim(-2.5, 2.5)
        ax.set_ylim(-2.5, 2.5)
        ax.set_zlim(-1.5, 1.5)
        
        X, Y, Z = r.mesh(i)
        z_norm = (Z - np.min(Z)) / (np.max(Z) - np.min(Z) + 1e-6)
        colors = plt.cm.magma(z_norm)
        
        ax.plot_surface(X, Y, Z, facecolors=colors, edgecolor="none", alpha=0.9, shade=True)
        t = i * 0.04
        ax.view_init(elev=20 + np.sin(t)*15, azim=i*3)
        writer.grab_frame()

print("Video 'saf_v41_REAKTIVE.mp4' fertig gerendert!")
PYEOF

echo "=== [3/4] Führe Audio-Synthese & Rendering aus ==="
python3 saf_audio_synth.py
python3 render_reaktiv.py

echo "=== [4/4] Verschiebe MP4 auf Desktop & Git-Sync ==="
mv saf_v41_REAKTIVE.mp4 ~/Desktop/ 2>/dev/null || true
find . -name ".DS_Store" -delete
echo ".DS_Store" >> .gitignore
git add .
git commit -m "feat(saf41): deploy audio-reactive vector pipeline and render reactive mp4" 2>/dev/null || true
git push origin main 2>/dev/null || true

echo "=== Gesamtausführung erfolgreich beendet! SAF V41.0 REAKTIV ist bereit. ==="
