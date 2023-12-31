
from genoma import Genoma
from harmonics import Harmonics, Scale
from midiutil import MIDIFile
from midi2audio import FluidSynth
import time
import json

class Sonification:
    def __init__(self, dna, scale=None, bmp=None, instruments=None, strategies=None, initial_octaves=None) -> None:
        
        # Initialize a Genoma instance if the 'dna' argument is a filepath.
        if type(dna) is str:
            dna = Genoma(dna)

        self.dna = dna
        self.instruments = instruments or [0, 32, 5, 75]
        self.frequency = dna.frequency(dna.mononucleotides())
        self.duration = round(len(dna.sequence()) / (self.frequency['G'] + self.frequency['C']) * 100)
        self.ratio = dna.ratio()
        self.bpm = bmp or int(self.ratio * 200)
        self.scaleName = scale or 'default'
        self.scale = getattr(Scale, self.scaleName)()
        self.strategies = strategies or ['apolar_codons', 'dinucleotides', 'polar_codons', 'basic_codons']
        self.initial_octaves = initial_octaves or [5, 1, 4, 3]
        
    def process(self) -> dict:
        """
        """
        outputFilename = self.dna.bio().id + '-' + str(time.time())
        
        frames = [
            getattr(self, self.strategies[0])(int(self.initial_octaves[0]), int(self.instruments[0])),
            getattr(self, self.strategies[1])(int(self.initial_octaves[1]), int(self.instruments[1])),
            getattr(self, self.strategies[2])(int(self.initial_octaves[2]), int(self.instruments[2])),
            getattr(self, self.strategies[3])(int(self.initial_octaves[3]), int(self.instruments[3])),
        ]

        # Building midi file
        midi = MIDIFile(
            numTracks=len(frames),
            
        )

        channel = 0
        track = 0

        for strings in frames:
            midi.addTempo(track=track, time=0, tempo=self.bpm)
            midi.addProgramChange(track, channel, 0, int(self.instruments[track]))

            for string in strings:
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
            'bmp': self.bpm,
            'strategies': self.strategies,
            'initial_octaves': self.initial_octaves,
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

    def all_start_stop(self, initial_octave, instrument) -> list:
        """
        """
        codons = self.dna.codons()
    
        mapping = Harmonics.map(
            items=codons,
            scale=self.scale,
            initial_octave=initial_octave
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
                
            velocity = self.ratio * frequencies[codons[i - 1]] if i > 1 else 100
            velocity = 127 if velocity > 127 else velocity
            velocity = velocity + 80 if velocity < 80 else velocity

            if not stopped:
                strings.append({
                    'value': codon,
                    'instrument': instrument,
                    'note': mapping[codon],
                    'velocity': int(velocity),
                    'time': i,
                    'duration': (self.ratio)
                })

            i += 1

        return strings
    
    def dinucleotides(self, initial_octave, instrument) -> list: # 32
        dinucleotides = self.dna.dinucleotides()
        frequencies = self.dna.frequency(dinucleotides)
        
        mapping = Harmonics.map(
            items=dinucleotides,
            scale=self.scale,
            initial_octave=initial_octave
        )

        mapping = Harmonics.to_midi(mapping)

        strings = list()

        i = 1
        for dinucleotide in dinucleotides:
            velocity = 32 + (frequencies[dinucleotides[i + 1]] / len(dinucleotides)) * 100 if i < len(dinucleotides) - 1 else 100
            velocity = 127 if velocity > 127 else velocity
            velocity = velocity + 80 if velocity < 80 else velocity
            
            strings.append({
                'value': dinucleotide,
                'instrument': instrument,
                'note': mapping[dinucleotide],
                'velocity': int(velocity),
                'time': i,
                'duration': (self.ratio)
            })

            i += 1

        return strings
    
    def polar_codons(self, initial_octave, instrument) -> list:
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
            initial_octave=initial_octave
        )

        mapping = Harmonics.to_midi(mapping)

        strings = list()

        i = 1
        for codon in codons:
            velocity = self.ratio * frequencies[codons[i - 1]] if i > 1 else 100
            velocity = 127 if velocity > 127 else velocity
            velocity = velocity + 80 if velocity < 80 else velocity

            if codon in polar_codons:
                strings.append({
                    'value': codon,
                    'instrument': instrument,
                    'note': mapping[codon],
                    'velocity': int(velocity),
                    'time': i,
                    'duration': (frequencies[codon] / len(frequencies)) * self.ratio
                })

            i += 1

        return strings
    
    def basic_codons(self, initial_octave, instrument) -> list:
        codons = self.dna.codons()
        frequencies = self.dna.frequency(codons)
        basic_codons = ['CAT', 'CAC', 'CGT', 'CGC', 'CGA', 'CGG']

        mapping = Harmonics.map(
            items=basic_codons,
            scale=self.scale,
            initial_octave=initial_octave
        )

        mapping = Harmonics.to_midi(mapping)

        strings = list()

        i = 1
        for codon in codons:
            velocity = self.ratio * frequencies[codons[i - 1]] if i > 1 else 100
            velocity = 127 if velocity > 127 else velocity
            velocity = velocity + 80 if velocity < 80 else velocity

            if codon in basic_codons:
                strings.append({
                    'value': codon,
                    'instrument': instrument,
                    'note': mapping[codon],
                    'velocity': int(velocity),
                    'time': i,
                    'duration': (frequencies[codon] / len(frequencies)) * self.ratio
                })

            i += 1

        return strings
    
    def apolar_codons(self, initial_octave, instrument) -> list:
        codons = self.dna.codons()
        frequencies = self.dna.frequency(codons)
        apolar_codons = [
            'TTT',
            'TTC',
            'TTA',
            'TTG',
            'CTT',
            'CTC',
            'CTA',
            'CTG',
            'ATT',
            'ATC',
            'ATA',
            'ATG',
            'GTT',
            'GTC',
            'GTA',
            'GTG',
            'CCT',
            'CCC',
            'CCA',
            'CCG',
            'GCT',
            'GCC',
            'GCA',
            'GCG',
            'TGG',
            'GGT',
            'GGC',
            'GGA',
            'GGG',
        ]

        mapping = Harmonics.map(
            items=apolar_codons,
            scale=self.scale,
            initial_octave=initial_octave
        )

        mapping = Harmonics.to_midi(mapping)

        strings = list()

        i = 1
        for codon in codons:
            velocity = self.ratio * frequencies[codons[i - 1]] if i > 1 else 100
            velocity = 127 if velocity > 127 else velocity
            velocity = velocity + 80 if velocity < 80 else velocity

            if codon in apolar_codons:
                strings.append({
                    'value': codon,
                    'instrument': instrument,
                    'note': mapping[codon],
                    'velocity': int(velocity),
                    'time': i,
                    'duration': (frequencies[codon] / len(frequencies)) * self.ratio
                })

            i += 1

        return strings
    
    def acidic_codons(self, initial_octave, instrument) -> list:
        codons = self.dna.codons()
        frequencies = self.dna.frequency(codons)
        acidic_codons = [
            'GAT',
            'GAC',
            'GAA',
            'GAG',
        ]

        mapping = Harmonics.map(
            items=acidic_codons,
            scale=self.scale,
            initial_octave=initial_octave
        )

        mapping = Harmonics.to_midi(mapping)

        strings = list()

        i = 1
        for codon in codons:
            velocity = self.ratio * frequencies[codons[i - 1]] if i > 1 else 100
            velocity = 127 if velocity > 127 else velocity
            velocity = velocity + 80 if velocity < 80 else velocity

            if codon in acidic_codons:
                strings.append({
                    'value': codon,
                    'instrument': instrument,
                    'note': mapping[codon],
                    'velocity': int(velocity),
                    'time': i,
                    'duration': (frequencies[codon] / len(frequencies)) * self.ratio
                })

            i += 1

        return strings