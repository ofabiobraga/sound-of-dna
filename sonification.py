
from genoma import Genoma
from harmonics import Harmonics, Scale
from midiutil import MIDIFile
from midi2audio import FluidSynth
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
        self.bmp = bmp or int(self.ratio * 200)
        self.scaleName = scale or 'default'
        self.scale = getattr(Scale, self.scaleName)()
        self.strategies = strategies or ['all_start_stop', 'dinucleotides', 'polar_codons', 'basic_start_stop']
        
    def process(self) -> dict:
        """
        """
        outputFilename = self.dna.bio().id + '-' + str(time.time())
        
        frames = [
            getattr(self, self.strategies[0])(),
            getattr(self, self.strategies[1])(),
            getattr(self, self.strategies[2])(),
            getattr(self, self.strategies[3])(),
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
                    duration=string['duration'],
                    volume=string['velocity']
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
            'strategies': self.strategies,
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
        
        for frame in frames:
            for string in frame:
                if not isinstance(string['instrument'], int):
                    print(string)
        
        # Saving as .json file
        with open('json/' + outputFilename + '.json', 'w') as jsonfile:
            json.dump(response, jsonfile)

        # Saving as .mid file
        with open('midi/' + outputFilename + '.mid', 'wb') as midifile:
            midi.writeFile(midifile)
            
        # Saving as .mp3 file
        # (FluidSynth()).midi_to_audio('midi/' + outputFilename + '.mid', 'mp3/' + outputFilename + '.mp3')

        return response

    def all_start_stop(self) -> list:
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
                    'instrument': int(self.instruments[0]),
                    'note': mapping[codon],
                    'velocity': 100,
                    'time': (self.ratio) * i,
                    'duration': (self.ratio)
                })

            i += 1

        return strings
    
    def dinucleotides(self) -> list: # 32
        dinucleotides = self.dna.dinucleotides()
        frequencies = self.dna.frequency(dinucleotides)
        
        mapping = Harmonics.map(
            items=dinucleotides,
            scale=self.scale,
            initial_octave=1
        )

        mapping = Harmonics.to_midi(mapping)

        strings = list()

        i = 1
        for dinucleotide in dinucleotides:
            velocity = 32 + frequencies[dinucleotides[i + 1]] / len(frequencies) if i < len(dinucleotides) - 1 else 100
            velocity = velocity if velocity < 255 else 255
            
            strings.append({
                'value': dinucleotide,
                'instrument': int(self.instruments[1]),
                'note': mapping[dinucleotide],
                'velocity': int(velocity),
                'time': (self.ratio) * i,
                'duration': (self.ratio)
            })

            i += 1

        return strings
    
    def polar_codons(self) -> list:
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
            velocity = self.ratio * frequencies[codons[i - 1]] if i > 1 else 100
            velocity = velocity if velocity < 255 else 255

            if codon in polar_codons:
                strings.append({
                    'value': codon,
                    'instrument': int(self.instruments[2]),
                    'note': mapping[codon],
                    'velocity': int(velocity),
                    'time': (self.ratio) * i,
                    'duration': (frequencies[codon] / len(frequencies)) * self.ratio
                })

            i += 1

        return strings
    
    def basic_start_stop(self) -> list:
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
                    'instrument': int(self.instruments[3]),
                    'note': mapping[codon],
                    'velocity': 100,
                    'time': (self.ratio) * i,
                    'duration': (frequencies[codon] / len(frequencies)) * self.ratio
                })

            i += 1

        return strings