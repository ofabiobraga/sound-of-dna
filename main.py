import sys
from genoma import Genoma
from harmonics import Harmonics, Scale
from sonification import Sonification
import mido
from midiutil import MIDIFile
from mido import MidiFile, MidiFile, MidiTrack

filepath = sys.argv[1]
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
print('. #1: Plucked Sweet Synth')
print('. #2: ---')
print('. #3: ---')
print('. #4: ---')


midi = MIDIFile(1)
midi.addTempo(track=0, time=0, tempo=120)

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

with open('output.mid', 'wb') as midifile:
    midi.writeFile(midifile)
    
midi_file = MidiFile('output.mid')
output_port = mido.open_output('SOD-Output', virtual=True)

for msg in midi_file.play():
    output_port.send(msg)

output_port.close()
