
from genoma import Genoma
from harmonics import Harmonics, Scale
from midiutil import MIDIFile
import time

class Sonification:
    def __init__(self, dna, scale=Scale.default()) -> None:
        
        # Initialize a Genoma instance if the 'dna' argument is a filepath.
        if type(dna) is str:
            dna = Genoma(dna)

        self.dna = dna
        self.scale = scale
        self.frequency = dna.frequency(dna.mononucleotides())
        self.duration = round(len(dna.sequence()) / (self.frequency['G'] + self.frequency['C']) * 100)
        self.ratio = dna.ratio()
        
    def process(self) -> dict:
        """
        """
        output = 'midi/' + self.dna.bio().id + '-' + str(time.time())
        
        frames = [
            self.one(),
            self.two(),
            self.three(),
            self.four()
        ]

        # Building midi file
        midi = MIDIFile(
            numTracks=len(frames)
        )

        channel = 0
        track = 0

        for strings in frames:
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

        # Saving as .mid file
        with open(output + '.mid', 'wb') as midifile:
            midi.writeFile(midifile)

        return {
            'id': self.dna.bio().id,
            'description': self.dna.bio().description,
            'frequencies': {
                'G': self.frequency['G'],
                'A': self.frequency['A'],
                'T': self.frequency['T'],
                'C': self.frequency['C'],
            },
            'gc/at': self.dna.ratio(),
            'midi': 'http://localhost:8000/' + output + '.mid',
            'codons': self.dna.codons(),
            'frames': frames
        }

    def one(self, instrument=112, scale=None) -> list:
        """
        """
        codons = self.dna.codons()
    
        mapping = Harmonics.map(
            items=codons,
            scale=scale or self.scale,
            initial_octave=2
        )

        mapping = Harmonics.to_midi(mapping)
        
        start_codons = ['ATG']
        stop_codons = ['TAA', 'TAG', 'TGA']
        stopped = True
        
        strings = list()
        
        i = 1
        for codon in codons:
            if stopped and codon in start_codons:
                stopped = False
                
            if not stopped and codon in stop_codons:
                stopped = True

            if not stopped:
                strings.append({
                    'value': codon,
                    'instrument': instrument,
                    'note': mapping[codon],
                    'volume': 100,
                    'time': (self.ratio) * i,
                    'velocity': (self.ratio)
                })

            i += 1

        return strings
    
    def two(self, instrument=32, scale=None) -> list: # 32
        dinucleotides = self.dna.dinucleotides()
        
        mapping = Harmonics.map(
            items=dinucleotides,
            scale=scale or self.scale,
            initial_octave=1
        )

        mapping = Harmonics.to_midi(mapping)

        strings = list()

        i = 1
        for dinucleotide in dinucleotides:
            strings.append({
                'value': dinucleotide,
                'instrument': instrument,
                'note': mapping[dinucleotide],
                'volume': 100,
                'time': (self.ratio) * i,
                'velocity': (self.ratio)
            })

            i += 1

        return strings
    
    def three(self, instrument=5, scale=None) -> list:
        codons = self.dna.codons()
        frequencies = self.dna.frequency(codons)
        polar_codons = [
            'TCT',
            'TCC',
            'TCA',
            'TCG',
            'ACT',
            'ACC',
            'ACA',
            'ACG',
            'TAT',
            'TAC',
            'CAA',
            'CAG',
            'AAT',
            'AAC',
            'TGT',
            'TGC',
            'AGT',
            'AGC',
        ]

        mapping = Harmonics.map(
            items=polar_codons,
            scale=scale or self.scale,
            initial_octave=4
        )

        mapping = Harmonics.to_midi(mapping)

        strings = list()

        i = 1
        for codon in codons:
            if codon in polar_codons:
                strings.append({
                    'value': codon,
                    'instrument': instrument,
                    'note': mapping[codon],
                    'volume': 100,
                    'time': (self.ratio) * i,
                    'velocity': (frequencies[codon] / len(frequencies)) * self.ratio
                })

            i += 1

        return strings
    
    def four(self, instrument=75, scale=None) -> list:
        codons = self.dna.codons()
        frequencies = self.dna.frequency(codons)
        basic_codons = ['CAT', 'CAC', 'CGT', 'CGC', 'CGA', 'CGG']
        start_codons = ['ATG']
        stop_codons = ['TAA', 'TAG', 'TGA']
        stopped = True

        i = 0
        for i in range(0, len(codons)):
            if codons[i] not in [*basic_codons, *start_codons, *stop_codons]:
                codons[i] = None

        mapping = Harmonics.map(
            items=codons,
            scale=scale or self.scale,
            initial_octave=4
        )

        mapping = Harmonics.to_midi(mapping)

        strings = list()

        i = 1
        for codon in codons:
            if stopped and codon in start_codons:
                stopped = False

            if not stopped and codon in stop_codons:
                stopped = True

            if not stopped and codon in basic_codons:
                strings.append({
                    'value': codon,
                    'instrument': instrument,
                    'note': mapping[codon],
                    'volume': 100,
                    'time': (self.ratio) * i,
                    'velocity': (frequencies[codon] / len(frequencies)) * self.ratio
                })

            i += 1

        return strings