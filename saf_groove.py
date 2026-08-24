import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter, sawtooth

# --- Parameter ---
SAMPLE_RATE = 44100
BPM = 120
BEATS = 32
SECONDS_PER_BEAT = 60 / BPM
TOTAL_DURATION = SECONDS_PER_BEAT * BEATS # 16 Sekunden
NUM_SAMPLES = int(SAMPLE_RATE * TOTAL_DURATION)

def get_t():
    return np.linspace(0, TOTAL_DURATION, NUM_SAMPLES, endpoint=False)

def export_wav(filename, audio_data):
    audio_int16 = (audio_data * 32767).astype(np.int16)
    wavfile.write(filename, SAMPLE_RATE, audio_int16)

# --- 1. SAF Spectral Fusion (Groove Carrier) ---
t = get_t()
white_noise = np.random.uniform(-1, 1, NUM_SAMPLES)

mod_freq = 1 / (4 * SECONDS_PER_BEAT)
spectral_mod = 0.5 * (1 + np.sin(2 * np.pi * mod_freq * t))
saf_groove = white_noise * spectral_mod

b, a = butter(5, 500 / (SAMPLE_RATE / 2), btype='high')
saf_groove = lfilter(b, a, saf_groove)

# --- 2. Feigenbaum-Dichtemuster (Spektral integriert) ---
N_FEIGENBAUM = NUM_SAMPLES
r = np.linspace(3.5, 4.0, N_FEIGENBAUM)
x = 0.5 * np.ones(N_FEIGENBAUM)
feigenbaum_pattern = np.zeros(N_FEIGENBAUM)

for i in range(1, N_FEIGENBAUM):
    x[i] = r[i] * x[i-1] * (1 - x[i-1])
    feigenbaum_pattern[i] = x[i]

feigenbaum_pattern = feigenbaum_pattern - np.mean(feigenbaum_pattern)
b_cha, a_cha = butter(5, [1800 / (SAMPLE_RATE / 2), 2200 / (SAMPLE_RATE / 2)], btype='band')
feigenbaum_chaos = lfilter(b_cha, a_cha, feigenbaum_pattern)

chaos_mod = 0.3 * (1 + np.sin(2 * np.pi * (mod_freq * 2) * t))
saf_with_chaos = saf_groove + (feigenbaum_chaos * chaos_mod * 0.2)

# --- 3. Vocoder-Morphed UP-Triolen ---
notes_freq = [130.81, 196.00, 261.63, 392.00] # C3, G3, C4, G4
triplet_beat_duration = (SECONDS_PER_BEAT / 3)
triplets_per_beat = 3
total_triplets = BEATS * triplets_per_beat

modulator_triplets = np.zeros(NUM_SAMPLES)
t_triplet = np.linspace(0, triplet_beat_duration, int(SAMPLE_RATE * triplet_beat_duration), endpoint=False)

for i in range(total_triplets):
    freq = notes_freq[i % len(notes_freq)]
    start_sample = int(i * SAMPLE_RATE * triplet_beat_duration)
    end_sample = start_sample + len(t_triplet)
    if end_sample > NUM_SAMPLES: break
    
    envelope = np.exp(-10 * t_triplet) 
    note = envelope * np.sin(2 * np.pi * freq * t_triplet)
    modulator_triplets[start_sample:end_sample] = note

num_saws = 7
supersaw = np.zeros(NUM_SAMPLES)
detune = 0.05
base_carrier_freq = 110 # A2

for i in range(num_saws):
    saw_freq = base_carrier_freq * (1 + np.random.uniform(-detune, detune))
    saw = sawtooth(2 * np.pi * saw_freq * t)
    supersaw += saw
supersaw = supersaw / num_saws

b1, a1 = butter(3, [650 / (SAMPLE_RATE / 2), 750 / (SAMPLE_RATE / 2)], btype='band')
f1_formant = lfilter(b1, a1, supersaw)
b2, a2 = butter(3, [1150 / (SAMPLE_RATE / 2), 1250 / (SAMPLE_RATE / 2)], btype='band')
f2_formant = lfilter(b2, a2, supersaw)
vocal_carrier = (f1_formant * 1.0) + (f2_formant * 0.7)

morph_curve = np.linspace(1.0, 0.0, NUM_SAMPLES)
morphed_carrier = (supersaw * morph_curve) + (vocal_carrier * (1 - morph_curve))

vocoded_triplets = morphed_carrier * np.abs(modulator_triplets)
vocoded_triplets = np.clip(vocoded_triplets * 1.5, -1, 1)

# --- 4. Finaler SAF Mix & Spatial Fusion ---
final_mix_L = (saf_with_chaos * 0.6) + (vocoded_triplets * 0.4)
final_mix_R = (saf_with_chaos * 0.4) + (vocoded_triplets * 0.6)

max_val = np.max(np.abs([final_mix_L, final_mix_R]))
final_mix_L /= max_val
final_mix_R /= max_val

final_stereo_mix = np.vstack((final_mix_L, final_mix_R)).T

output_filename = "saf_spectral_groove_32beats.wav"
print(f"[SAF] Generiere {output_filename}...")
export_wav(output_filename, final_stereo_mix)
print("[SAF] Synthese erfolgreich abgeschlossen!")
