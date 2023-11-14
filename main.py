import sys
from genoma import Genoma
from sonification import Sonification

filepath = sys.argv[1]
dna = Genoma(filepath)

Sonification(dna).process()

# Todo: Add outputs to the console about the DNA and Sonification
