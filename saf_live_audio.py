import time
import json
import asyncio
import numpy as np
import websockets

try:
    import sounddevice as sd
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False

class SAFFrameworkLive:
    def __init__(self):
        self.version = "V33.4"
        self.fade_counter = 128
        self.latency_ms = 0.0
        self.rms = 0.0
        self.fft_bins = [0.0, 0.0, 0.0, 0.0]
        self.latest_metrics = {}

    def process_audio_chunk(self, indata):
        start_time = time.perf_counter()
        
        audio_flat = np.mean(indata, axis=1) if indata.ndim > 1 and indata.shape[1] > 1 else indata[:, 0]

        fft_data = np.abs(np.fft.rfft(audio_flat))
        if len(fft_data) >= 4:
            chunk_size = len(fft_data) // 4
            self.fft_bins = [
                float(np.mean(fft_data[0:chunk_size])),
                float(np.mean(fft_data[chunk_size:2*chunk_size])),
                float(np.mean(fft_data[2*chunk_size:3*chunk_size])),
                float(np.mean(fft_data[3*chunk_size:]))
            ]

        if self.fade_counter > 0:
            self.fade_counter -= 1
        else:
            self.fade_counter = 128

        end_time = time.perf_counter()
        self.latency_ms = (end_time - start_time) * 1000.0
        self.rms = float(np.sqrt(np.mean(audio_flat**2)))

        self.latest_metrics = {
            "fade_counter": self.fade_counter,
            "rms": round(self.rms, 4),
            "fft": [round(b, 2) for b in self.fft_bins],
            "latency_ms": round(self.latency_ms, 2)
        }
        return self.latest_metrics

if __name__ == "__main__":
    saf = SAFFrameworkLive()

    if not AUDIO_AVAILABLE:
        print("Fehler: sounddevice Modul fehlt.")
        exit(1)

    print("\n--- Verfügbare Audiogeräte ---")
    print(sd.query_devices())
    print("------------------------------\n")

    try:
        dev_id = int(input("[SAF] ID des Eingabegeräts wählen (z.B. BlackHole = 2): "))
    except ValueError:
        dev_id = sd.default.device[0]

    device_info = sd.query_devices(dev_id)
    print(f"\n[SAF] Verbunden mit: {device_info['name']}")
    print("[SAF] Starte WebSocket-Server auf ws://localhost:8765 ...\n")

    def audio_callback(indata, frames, time_info, status):
        metrics = saf.process_audio_chunk(indata)
        print(f"RMS: {metrics['rms']:.4f} | FFT Bass: {metrics['fft'][0]:.1f} | Latenz: {metrics['latency_ms']} ms", end='\r')

    async def handler(websocket):
        while True:
            if saf.latest_metrics:
                await websocket.send(json.dumps(saf.latest_metrics))
            await asyncio.sleep(0.03)

    async def main():
        stream = sd.InputStream(device=dev_id, channels=2, callback=audio_callback, blocksize=1024, samplerate=44100)
        with stream:
            async with websockets.serve(handler, "localhost", 8765):
                await asyncio.Future()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[SAF] Live-Analyse beendet.")
