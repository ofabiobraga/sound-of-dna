import sys
import time
from genoma import Genoma
from harmonics import Harmonics, Scale
from sonification import Sonification
from midiutil import MIDIFile

filepath = sys.argv[1]
output = './midi/'+ str(time.time()) + '.mid'
harmonics = Harmonics()
scale = Scale()

# DNA attributes
dna = Genoma(filepath)
mononucleotides = dna.mononucleotides()
dinucleotides = dna.dinucleotides()
codons = dna.codons()
frequency = dna.frequency(mononucleotides)
ratio = dna.ratio()

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

print('[ Frames ]')
print('. #1 (Lead) Plucked Sweet Synth, Fairytales Bells')
print('. #2 (Bass) Upright Studio Bass, Simple Physics Piano')
print('. #3 (Percursion) ---')
print('. #4 (Piano FX) ---')
print('. #5 (Special FX) Breathy Vox, Drifting Away, Glass Sky')
print('. #6 (Drum Metals) ---')


midi = MIDIFile(3)
midi.addTempo(track=0, time=0, tempo=90)
midi.addTempo(track=1, time=0, tempo=90)
midi.addTempo(track=2, time=0, tempo=90)

sonification = Sonification(dna)

# Building lead track
for string in sonification.lead():
    midi.addProgramChange(0, 0, 0, string['instrument'])
    midi.addNote(
        pitch=string['note'],
        track=0,
        channel=0,
        time=string['time'],
        duration=string['velocity'],
        volume=string['volume']
    )

# Building bass track
for string in sonification.bass():
    midi.addProgramChange(0, 0, 0, string['instrument'])
    midi.addNote(
        pitch=string['note'],
        track=1,
        channel=1,
        time=string['time'],
        duration=string['velocity'],
        volume=string['volume']
    )

# Building Special FX track
for string in sonification.special_fx():
    midi.addProgramChange(0, 0, 0, string['instrument'])
    midi.addNote(
        pitch=string['note'],
        track=2,
        channel=2,
        time=string['time'],
        duration=string['velocity'],
        volume=string['volume']
    )

with open(output, 'wb') as midifile:
    midi.writeFile(midifile)
