# This file applies the huffman encoding to bytecode from a specific contract
import os
from huffman import HuffmanCoding

# input file path
path = "bytecode.txt"

h = HuffmanCoding()
for filename in os.listdir("contracts"):
    with open("contracts/" + filename, 'r') as file:
        text = file.read().rstrip()
        h.make_frequency_dict(text)
for filename in os.listdir("contracts"):
    path = "contracts/" + filename
    h.compress(path)

print(h.saved)
