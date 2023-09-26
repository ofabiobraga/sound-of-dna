import Bio.SeqIO

class Genoma:
    def __init__(self, filepath):
        self.__raw = Bio.SeqIO.read(filepath, 'fasta')
        self.__sequence = self.__raw.seq
        
    def sequence(self):
        """
        """
        return str(self.__sequence)
        
    def mononucleotides(self):
        """
        """
        return list(self.__sequence)
    
    def dinucleotides(self):
        """
        """
        return self.__group(2)
    
    def codons(self):
        """
        """
        return self.__group(3)
    
    def frequency(self, set):
        """
        """
        frequencies = dict()

        for item in set:
            frequencies[item] = frequencies.get(item, 0) + 1

        return dict(sorted(frequencies.items()))
    
    def ratio(self):
        frequencies = self.frequency(self.mononucleotides())
        
        gc = frequencies['G'] + frequencies['C']
        at = frequencies['A'] + frequencies['T']

        return round(gc / at, 3)
    
    def __group(self, size):
        """
        """
        nucleotides = self.sequence()
        groups = list()

        for i in range(0, len(nucleotides), size):
            groups.append(nucleotides[i:i + size])

        return groups
