# This file applies the huffman encoding to bytecode from a specific contract
import os
from huffman import HuffmanCoding
from compare import verify
from rle import encode, decode

# input file path
total_cmp = 0
total_len = 0
h = HuffmanCoding(2)

for filename in os.listdir("contracts"):
    with open("contracts/" + filename, 'r') as file:
        text = file.read().rstrip()
        total_len += len(text)
        h.make_frequency_dict(text)


# compressing all contracts
for filename in os.listdir("contracts"):
    with open("contracts/" + filename, 'r') as input, open("compressed_contracts/" + filename, 'w') as output:
        compressed = h.compress(input.read())
        total_cmp += len(compressed)
        output.write(compressed)

saved = total_len - total_cmp

print("Total chars saved: " + str(saved))
print("Compression rate: " + str(saved * 100/total_len) + "%")

# decompressing all contracts
for filename in os.listdir("compressed_contracts"):
    with open("compressed_contracts/" + filename, "r") as input, open("decompressed_contracts/" + filename, 'w') as output:
        text = input.read()
        decompressed = h.decompress(text)
        if len(decompressed) == 0:
            print(len(text))
        output.write(decompressed)

# verify()
