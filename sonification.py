
from genoma import Genoma
from harmonics import Harmonics, Scale

class Sonification:
    def __init__(self, dna: Genoma, scale=Scale.default()) -> None:
        self.dna = dna
        self.scale = scale
        self.frequency = dna.frequency(dna.mononucleotides())
        self.duration = round(len(dna.sequence()) / (self.frequency['G'] + self.frequency['C']) * 100)
        self.ratio = dna.ratio()

    def lead(self, instrument=0, scale=None) -> list:
        """
        """
        codons = self.dna.codons()
    
        mapping = Harmonics.map(
            items=codons,
            scale=scale or self.scale,
            initial_octave=2
        )

        mapping = Harmonics.to_midi(mapping)
        
        strings = list()
        
        i = 1
        for codon in codons:
            strings.append({
                'instrument': instrument,
                'note': mapping[codon],
                'volume': 100,
                'time': (1 - self.ratio) * i,
                'velocity': 100
            })

            i += 1
        
        return strings
    
    def bass(self, instrument=0) -> list:
        return list()
    
    def percussion(self, instrument=0) -> list:
        return list()
    
    def piano_fx(self, instrument=0) -> list:
        return list()
    
    def special_fx(self, instrument=0) -> list:
        return list()
    
    def drum_metals(self, instrument=0) -> list:
        return list()