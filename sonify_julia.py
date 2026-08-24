import numpy as np
from PIL import Image
from scipy.io import wavfile

img = Image.open("julia_parameters_4_panel_2.jpg").convert("L").resize((400, 200))
audio_data = (np.array(img, dtype=np.float32).flatten() - 127.5) / 127.5
wavfile.write("julia_sonification.wav", 22050, (audio_data * 32767).astype(np.int16))
print("Fertig!")
