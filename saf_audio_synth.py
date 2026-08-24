import numpy as np
import wave
import struct

class SAF41AudioEngine:
    def __init__(self, bpm=87.273, sample_rate=44100):
        self.bpm = bpm
        self.sr = sample_rate
        self.feigenbaum = np.array([0.987, 0.933, 0.937, 0.954])
        self.phase_shift = np.pi / 2.0
        
        # Dauer: Genau 8 Bars bei 87.273 BPM
        # 1 Bar (4/4) bei 87.273 BPM = 60 / 87.273 * 4 ≈ 2.7502 Sek
        # 8 Bars ≈ 22.0016 Sekunden
        self.seconds_per_bar = (60.0 / self.bpm) * 4.0
        self.duration = self.seconds_per_bar * 8.0 
        self.num_samples = int(self.sr * self.duration)

    def generate_stems(self):
        t_vec = np.linspace(0, self.duration, self.num_samples, endpoint=False)
        
        # Fundamental-Frequenzen basierend auf SAF-Resonanzen
        f_sub = 87.273 / 2.0  # ~43.636 Hz (Sub Sub-Bass)
        f_mid = f_sub * 3.0   # ~130.909 Hz (Mid-Harmonics)
        f_high = f_sub * 8.0  # ~349.091 Hz (High Spatial Vector)

        # 1. STEM 1: Sub Bass (Z-Achsen Phasenwellenform)
        z_mod = np.sin(2 * np.pi * f_sub * t_vec + self.phase_shift * np.cos(t_vec * 0.5))
        stem_sub = 0.7 * np.tanh(z_mod * 1.5) # Soft Clipping

        # 2. STEM 2: Mid Resonanz (Feigenbaum FM Modulation)
        fm_mod = np.sin(2 * np.pi * (f_mid * self.feigenbaum[0]) * t_vec + 
                        np.sin(2 * np.pi * (f_mid * self.feigenbaum[1]) * t_vec))
        stem_mid = 0.5 * fm_mod * (0.8 + 0.2 * np.sin(2 * np.pi * (self.bpm / 60.0) * t_vec))

        # 3. STEM 3: High Spatial Phase (D1-D6 Vector Sweep)
        phase_sweep = np.sin(2 * np.pi * f_high * t_vec + self.feigenbaum[2] * np.sin(t_vec * 2.0))
        stem_high = 0.3 * phase_sweep * np.cos(np.pi * t_vec / self.seconds_per_bar)

        return stem_sub, stem_mid, stem_high

    def save_wav(self, filename, audio_data):
        # Normalize to -1.0 .. 1.0
        max_val = np.max(np.abs(audio_data))
        if max_val > 0:
            audio_data = audio_data / max_val * 0.95

        packed_data = bytearray()
        for s in audio_data:
            val = int(s * 32767)
            packed_data.extend(struct.pack('<h', val))

        with wave.open(filename, 'w') as f:
            f.setnchannels(1) # Mono PCM
            f.setsampwidth(2) # 16-bit
            f.setframerate(self.sr)
            f.writeframes(packed_data)
        print(f"Exportiert: {filename}")

if __name__ == "__main__":
    synth = SAF41AudioEngine(bpm=87.273)
    print(f"Synthetisiere SAF V41.0 Audio Stems ({synth.duration:.3f} s @ 87.273 BPM)...")
    sub, mid, high = synth.generate_stems()
    
    synth.save_wav("saf_stem1_sub_87.273bpm.wav", sub)
    synth.save_wav("saf_stem2_mid_87.273bpm.wav", mid)
    synth.save_wav("saf_stem3_high_87.273bpm.wav", high)
    
    # Master Mixdown
    master = (sub * 0.5) + (mid * 0.3) + (high * 0.2)
    synth.save_wav("saf_master_mix_87.273bpm.wav", master)
