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
    'sonification': {
        'lead': sonification.lead(),
        'bass': sonification.bass(),
        'special_fx': sonification.special_fx(),
    },
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
print('. G: ' + str(frequency['G']))
print('. A: ' + str(frequency['A']))
print('. T: ' + str(frequency['T']))
print('. C: ' + str(frequency['C']))
print('')

# Ratios
print('[ Ratio ]')
print('. GC/AT: ' + str(ratio))
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
midi = MIDIFile(3)
midi.addTempo(track=0, time=0, tempo=90)
midi.addTempo(track=1, time=0, tempo=90)
midi.addTempo(track=2, time=0, tempo=90)

# Building Lead track
for string in info['sonification']['lead']:
    midi.addProgramChange(0, 0, 0, string['instrument'])
    midi.addNote(
        pitch=string['note'],
        track=0,
        channel=0,
        time=string['time'],
        duration=string['velocity'],
        volume=string['volume']
    )

# Building Bass track
for string in info['sonification']['bass']:
    midi.addProgramChange(1, 1, 0, string['instrument'])
    midi.addNote(
        pitch=string['note'],
        track=1,
        channel=1,
        time=string['time'],
        duration=string['velocity'],
        volume=string['volume']
    )

# Building Special FX track
for string in info['sonification']['special_fx']:
    midi.addProgramChange(2, 2, 0, string['instrument'])
    midi.addNote(
        pitch=string['note'],
        track=2,
        channel=2,
        time=string['time'],
        duration=string['velocity'],
        volume=string['volume']
    )

# Building Percussion track (to-do)
# Building Piano FX (to-do)
# Building Drum Metals track (to-do)

# Saving as .json file
with open(output + '.json', 'w') as jsonfile:
    json.dump(info, jsonfile)

# Saving as .mid file
with open(output + '.mid', 'wb') as midifile:
    midi.writeFile(midifile)
