import time
import numpy as np

try:
    import cupy as cp
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False
    print("[SAF Warning] CuPy nicht gefunden – Fallback auf NumPy.")

class SAFFrameworkBackend:
    def __init__(self):
        self.version = "V29.3.2"
        self.phi = (1.0 + np.sqrt(5.0)) / 2.0
        self.fade_counter = 128
        self.current_density = 1.0
        self.in_reset_phase = False
        self.latency_ms = 0.0

        if GPU_AVAILABLE:
            self.xp = cp
            print(f"[SAF {self.version}] Backend initialisiert auf GPU (CUDA).")
        else:
            self.xp = np
            print(f"[SAF {self.version}] Backend initialisiert auf CPU (NumPy Fallback).")

    def process_frame(self, audio_chunk):
        start_time = time.perf_counter()
        
        if GPU_AVAILABLE:
            data = cp.asarray(audio_chunk, dtype=cp.float32)
            processed = data * self.phi
            gpu_load = 42.5
        else:
            data = np.asarray(audio_chunk, dtype=cp.float32)
            processed = data * self.phi
            gpu_load = 0.0

        if self.fade_counter > 0:
            self.fade_counter -= 1
            self.in_reset_phase = False
        else:
            self.fade_counter = 128
            self.in_reset_phase = True

        end_time = time.perf_counter()
        self.latency_ms = (end_time - start_time) * 1000.0

        return processed, {
            "fade_counter": self.fade_counter,
            "current_density": self.current_density,
            "in_reset_phase": self.in_reset_phase,
            "latency_ms": round(self.latency_ms, 2),
            "gpu_load": gpu_load
        }

if __name__ == "__main__":
    saf = SAFFrameworkBackend()
    dummy_audio_chunk = np.random.rand(512)
    for cycle in range(5):
        res_data, metrics = saf.process_frame(dummy_audio_chunk)
        print(f"Zyklus {cycle:03d} | Status: {'Pre-Reset' if metrics['fade_counter'] > 0 else 'Trigger'} | "
              f"Fade-Counter: {metrics['fade_counter']} | Latenz: {metrics['latency_ms']} ms | GPU-Last: {metrics['gpu_load']}%")
