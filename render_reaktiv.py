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
