import math
from audiolazy import str2midi


class Scale:
    def chromatic(self):
        return ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    def blues(self):
        return ['A', 'C', 'D', 'D#', 'E', 'G']
    
    def a_sharp(self):
        return ['F#', 'G#', 'A', 'B', 'C#', 'D', 'A#']
    
    def d_sharp_minor_harmonic(self):
        return ['C', 'D', 'D#', 'F', 'G', 'G#', 'A#']

class Harmonics:
    def map(self, items, scale=Scale().chromatic(), initial_octave=0):
        mapping = {element: None for element in items}
        octave = initial_octave

        i = 0
        for element in mapping:
            mapping[element] = scale[i] + str(octave)
            i += 1
            
            if i == len(scale):
                octave += 1
                i = 0
                
        return mapping
    
    def to_midi(self, mapping):
        notes = dict()
        for key, note in mapping.items():
            midi = str2midi(note)
            
            if midi > 127:
                midi = round(midi/2)
                
            notes[key] = midi

        return notes
    

