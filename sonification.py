
from genoma import Genoma
from harmonics import Harmonics, Scale

class Sonification:
    def __init__(self, dna: Genoma, scale=Scale.default()) -> None:
        self.dna = dna
        self.scale = scale
        self.frequency = dna.frequency(dna.mononucleotides())
        self.duration = round(len(dna.sequence()) / (self.frequency['G'] + self.frequency['C']) * 100)
        self.ratio = dna.ratio()

    def lead(self, instrument=83, scale=None) -> list:
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
                    'time': (1 - self.ratio) * i,
                    'velocity': (1 - self.ratio)
                })

            i += 1

        return strings
    
    def bass(self, instrument=33, scale=None) -> list:
        dinucleotides = self.dna.dinucleotides()
        
        mapping = Harmonics.map(
            items=dinucleotides,
            scale=scale or self.scale,
            initial_octave=0
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
                'time': (1 - self.ratio) * i,
                'velocity': (1 - self.ratio)
            })

            i += 1

        return strings
    
    def percussion(self, instrument=0) -> list:
        return list()
    
    def piano_fx(self, instrument=0) -> list:
        return list()
    
    def special_fx(self, instrument=0, scale=None) -> list:
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
                    'time': (1 - self.ratio) * i,
                    'velocity': (frequencies[codon] / len(frequencies)) * self.ratio
                })

            i += 1

        return strings
    
    def drum_metals(self, instrument=0) -> list:
        return list()