import mido
from mido import Message, MidiFile, MidiTrack

def save_bifurcation_to_midi(bifurcation_points, filename="saf_bifurcation.mid"):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    
    # Mapping der Bifurkationspunkte auf MIDI-Noten (A-B linear aufgelöst)
    for point in bifurcation_points:
        # Hier wird die mathematische Instabilität in eine MIDI-Note übersetzt
        note = int(60 + (point * 12)) 
        track.append(Message('note_on', note=note, velocity=64, time=480))
        track.append(Message('note_off', note=note, velocity=64, time=480))
    
    mid.save(filename)
    print(f"MIDI-Struktur für {filename} erfolgreich generiert.")import time
r = 3.5
# Exponentieller Fokus auf den kritischen Bereich
step = 0.001
while r < 3.571:
    with open('saf_data/r_val', 'w') as f: f.write(f"{r:.7f}")
    # Schrittweite verfeinern für maximale Präzision bei 3.57
    step *= 0.99
    r += step
    time.sleep(0.01)
