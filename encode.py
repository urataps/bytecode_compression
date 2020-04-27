# This file applies the huffman encoding to bytecode from a specific contract
import os
from huffman import HuffmanCoding
from compare import verify

# input file path
path = "bytecode.txt"

total_len = 0
h = HuffmanCoding()

for filename in os.listdir("contracts"):
    with open("contracts/" + filename, 'r') as file:
        text = file.read().rstrip()
        total_len += len(text)
        h.make_frequency_dict(text)

# injecting a new contract from which entropy was not based on
with open('contracts/0x521A2aC7b33b09fA21A1aD7C040F4e1b5912C1d0.evm', 'w') as file:
    file.write("600080546001600160a01b0319163317905560c0604052600560808190527f7a5455534400000000000000000000000000000000000000000000000000000060a09081526200005291600291906200011a")

# compressing all contracts
for filename in os.listdir("contracts"):
    with open("contracts/" + filename, 'r') as input, open("compressed_contracts/" + filename, 'w') as output:
        output.write(h.compress(input.read()))


print("Total chars saved: " + str(h.saved))
print("Compression rate: " + str(h.saved * 100/total_len) + "%")

# decompressing all contracts
for filename in os.listdir("compressed_contracts"):
    with open("compressed_contracts/" + filename, "r") as input, open("decompressed_contracts/" + filename, 'w') as output:
        text = input.read()
        output.write(h.decompress(text))

verify()
