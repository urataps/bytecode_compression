from compare import verify
from sequence import dict, independent, isAtom
from hybridHuff import HuffmanCoding
import os


# This function assumes the 2 dictionaries are disjoint
def addDicts(d1, d2):
    result = {}
    for key in d1:
        result[key] = d1[key]
    for key in d2:
        result[key] = d2[key]
    return result


h = HuffmanCoding(2)

total_len = 0
total_cmp = 0


for filename in os.listdir("contracts"):
    with open("contracts/" + filename, 'r') as file:
        text = file.read().rstrip()
        total_len += len(text)
        h.make_frequency_dict(text)


# dict = independent(dict)
h.freq = addDicts(h.freq, dict)

# h.freq = independent(h.freq)
h.make_tree()

while True:
    redundant = h.isOptimal()
    if redundant == True:
        break
    else:
        if redundant in h.freq:
            del h.freq[redundant]
    h.make_tree()

h.make_trie()


# compressing all contracts
for filename in os.listdir("contracts"):
    with open("contracts/" + filename, 'r') as input, open("hybridcompressed_contracts/" + filename, 'w') as output:
        compressed = h.compress(input.read())
        total_cmp += len(compressed)
        output.write(compressed)

saved = total_len - total_cmp

print("Total chars saved: " + str(saved))
print("Compression rate: " + str(saved * 100/total_len) + "%")

# decompressing all contracts
for filename in os.listdir("hybridcompressed_contracts"):
    with open("hybridcompressed_contracts/" + filename, "r") as input, open("hybriddecompressed_contracts/" + filename, 'w') as output:
        text = input.read()
        decompressed = h.decompress(text)
        output.write(decompressed)


verify()

with open("sequences.txt", 'w') as file:
    s = ''

    for key in {k: v for k, v in sorted(h.freq.items(), key=lambda item: item[1], reverse=True)}:
        s += key + ' : ' + h.codes[key] + ' : ' + str(h.freq[key]) + '\n'

    file.write(s)
