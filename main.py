import sys
import time
from genoma import Genoma
from harmonics import Harmonics, Scale
from sonification import Sonification
import mido
from midiutil import MIDIFile
from mido import MidiFile, MidiFile, MidiTrack

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
print('. #2 (Bass) Upright Studio Bass')
print('. #3 (Percursion) ---')
print('. #4 (Piano FX) ---')
print('. #5 (Special FX) ---')
print('. #6 (Drum Metals) ---')


midi = MIDIFile(2)
midi.addTempo(track=0, time=0, tempo=90)
midi.addTempo(track=1, time=0, tempo=90)

# Defining instruments
midi.addProgramChange(0, 0, 0, 83)
midi.addProgramChange(1, 1, 0, 33)

# Building lead track
for string in Sonification(dna).lead():
    midi.addNote(
        pitch=string['note'],
        track=0,
        channel=0,
        time=string['time'],
        duration=string['velocity'],
        volume=string['volume']
    )
    
# Building bass track
for string in Sonification(dna).bass():
    midi.addNote(
        pitch=string['note'],
        track=1,
        channel=1,
        time=string['time'],
        duration=string['velocity'],
        volume=string['volume']
    )

with open(output, 'wb') as midifile:
    midi.writeFile(midifile)
    
midi_file = MidiFile(output)
output_port = mido.open_output('SOD-Output', virtual=True)

for msg in midi_file.play():
    output_port.send(msg)

output_port.close()
