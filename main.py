import sys
import time
import json
from genoma import Genoma
from harmonics import Harmonics, Scale
from sonification import Sonification
from midiutil import MIDIFile

filepath = sys.argv[1]
harmonics = Harmonics()
scale = Scale()
dna = Genoma(filepath)

# DNA attributes
mononucleotides = dna.mononucleotides()
dinucleotides = dna.dinucleotides()
codons = dna.codons()
frequency = dna.frequency(mononucleotides)
ratio = dna.ratio()

# Sonification attributes
sonification = Sonification(dna)

info = {
    'id': dna.bio().id,
    'description': dna.bio().description,
    'codons': dna.codons(),
    'frequencies': {
        'G': frequency['G'],
        'A': frequency['A'],
        'T': frequency['T'],
        'C': frequency['C'],
    },
    'gc/at': ratio,
    'sonification': [
        sonification.one(),
        sonification.two(),
        sonification.three(),
        sonification.four(),
    ],
}

output = './midi/' + info['id'] + '-' + str(time.time())

# Lengths of each sequence
print('[ Lengths of each sequence ]')
print('. Mono-Nucleotides: ' + str(len(mononucleotides)))
print('. Di-Nucleotides: ' + str(len(dinucleotides)))
print('. Codons: ' + str(len(codons)))
print('')

# Frequency of each nucleotide
print('[ Frequency of each nucleotide ]')
print('. G: ' + str(info['frequencies']['G']))
print('. A: ' + str(info['frequencies']['A']))
print('. T: ' + str(info['frequencies']['T']))
print('. C: ' + str(info['frequencies']['C']))
print('')

# Ratios
print('[ Ratio ]')
print('. GC/AT: ' + str(info['gc/at']))
print('')

# Frames
print('[ Frames ]')
print('. #1 (Lead) Plucked Sweet Synth, Fairytales Bells')
print('. #2 (Bass) Upright Studio Bass, Simple Physics Piano')
print('. #3 (Percursion) ---')
print('. #4 (Piano FX) ---')
print('. #5 (Special FX) Breathy Vox, Drifting Away, Glass Sky, Worn Tape Piano')
print('. #6 (Drum Metals) ---')

# Building midi file
midi = MIDIFile(
    numTracks=len(info['sonification'])
)

channel = 0
track = 0

for strings in info['sonification']:
    midi.addTempo(track=track, time=0, tempo=140)

    for string in strings:
        midi.addProgramChange(track, channel, 0, string['instrument'])
        midi.addNote(
            pitch=string['note'],
            track=track,
            channel=channel,
            time=string['time'],
            duration=string['velocity'],
            volume=string['volume']
        )

    channel += 1
    track += 1

# Saving as .json file
with open(output + '.json', 'w') as jsonfile:
    json.dump(info, jsonfile)

# Saving as .mid file
with open(output + '.mid', 'wb') as midifile:
    midi.writeFile(midifile)
