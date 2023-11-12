
from genoma import Genoma
from harmonics import Harmonics, Scale
from midiutil import MIDIFile
import time
import json

class Sonification:
    def __init__(self, dna, scale=None, bmp=None, instruments=None, strategies=None) -> None:
        
        # Initialize a Genoma instance if the 'dna' argument is a filepath.
        if type(dna) is str:
            dna = Genoma(dna)

        self.dna = dna
        self.instruments = instruments or [112, 32, 5, 75]
        self.frequency = dna.frequency(dna.mononucleotides())
        self.duration = round(len(dna.sequence()) / (self.frequency['G'] + self.frequency['C']) * 100)
        self.ratio = dna.ratio()
        self.bmp = bmp or 140
        self.scaleName = scale or 'default'
        self.scale = getattr(Scale, self.scaleName)()
        
    def process(self) -> dict:
        """
        """
        outputFilename = self.dna.bio().id + '-' + str(time.time())
        
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
            midi.addTempo(track=track, time=0, tempo=self.bmp)

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
            
        response = {
            'id': self.dna.bio().id,
            'description': self.dna.bio().description,
            'frequencies': {
                'G': self.frequency['G'],
                'A': self.frequency['A'],
                'T': self.frequency['T'],
                'C': self.frequency['C'],
            },
            'length': len(self.dna.sequence()),
            'gc/at': self.dna.ratio(),
            'scale': self.scaleName,
            'bmp': self.bmp,
            'mp3': {
                'filename': outputFilename + '.mp3',
                'url':  'http://localhost:8000/mp3/' + outputFilename + '.mp3'
            },
            'midi': {
                'filename': outputFilename + '.mid',
                'url': 'http://localhost:8000/midi/' + outputFilename + '.mid'
            },
            'json' : {
                'filename': outputFilename + '.json',
                'url': 'http://localhost:8000/json/' + outputFilename + '.json'
            },
            'codons': self.dna.codons(),
            'frames': frames
        }
        
        # Saving as .json file
        with open('json/' + outputFilename + '.json', 'w') as jsonfile:
            json.dump(response, jsonfile)

        # Saving as .mid file
        with open('midi/' + outputFilename + '.mid', 'wb') as midifile:
            midi.writeFile(midifile)

        return response

    def one(self) -> list:
        """
        """
        codons = self.dna.codons()
    
        mapping = Harmonics.map(
            items=codons,
            scale=self.scale,
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
                    'instrument': self.instruments[0],
                    'note': mapping[codon],
                    'volume': 100,
                    'time': (self.ratio) * i,
                    'velocity': (self.ratio)
                })

            i += 1

        return strings
    
    def two(self) -> list: # 32
        dinucleotides = self.dna.dinucleotides()
        
        mapping = Harmonics.map(
            items=dinucleotides,
            scale=self.scale,
            initial_octave=1
        )

        mapping = Harmonics.to_midi(mapping)

        strings = list()

        i = 1
        for dinucleotide in dinucleotides:
            strings.append({
                'value': dinucleotide,
                'instrument': self.instruments[1],
                'note': mapping[dinucleotide],
                'volume': 100,
                'time': (self.ratio) * i,
                'velocity': (self.ratio)
            })

            i += 1

        return strings
    
    def three(self) -> list:
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
            scale=self.scale,
            initial_octave=4
        )

        mapping = Harmonics.to_midi(mapping)

        strings = list()

        i = 1
        for codon in codons:
            if codon in polar_codons:
                strings.append({
                    'value': codon,
                    'instrument': self.instruments[2],
                    'note': mapping[codon],
                    'volume': 100,
                    'time': (self.ratio) * i,
                    'velocity': (frequencies[codon] / len(frequencies)) * self.ratio
                })

            i += 1

        return strings
    
    def four(self) -> list:
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
            scale=self.scale,
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
                    'instrument': self.instruments[3],
                    'note': mapping[codon],
                    'volume': 100,
                    'time': (self.ratio) * i,
                    'velocity': (frequencies[codon] / len(frequencies)) * self.ratio
                })

            i += 1

        return strings