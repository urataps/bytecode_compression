from compare import verify
from sequence import dict
from hybridHuff import HuffmanCoding
from tqdm import tqdm
import time
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


for filename in tqdm(os.listdir("contracts")):
    with open("contracts/" + filename, 'r') as file:
        text = file.read().rstrip()
        h.make_frequency_dict(text)


h.freq = addDicts(h.freq, dict)
h.make_tree()

# verify that no code is longer than the sequence
while True:
    redundant = h.isOptimal()
    print(len(h.codes))
    if redundant == True:
        break
    else:
        if redundant in h.codes:
            del h.codes[redundant]


h.make_trie()


localtime = time.asctime(time.localtime(time.time()))
print("Compression Started: " + localtime)
# compressing all contracts
for filename in tqdm(os.listdir("contracts")):
    with open("contracts/" + filename, 'r') as input, open("hybridcompressed_contracts/" + filename, 'w') as output:
        text = input.read().rstrip()
        total_len += len(text)
        compressed = h.compress(text)
        total_cmp += len(compressed)
        output.write(compressed)

saved = total_len - total_cmp
print("Total chars saved: " + str(saved))
print("Compression rate: " + str(saved * 100/total_len) + "%")
localtime = time.asctime(time.localtime(time.time()))
print(" Copmresion Finished: " + localtime)
localtime = time.asctime(time.localtime(time.time()))
print("Decompression Started: " + localtime)
# decompressing all contracts
for filename in tqdm(os.listdir("hybridcompressed_contracts")):
    with open("hybridcompressed_contracts/" + filename, "r") as input, open("hybriddecompressed_contracts/" + filename, 'w') as output:
        text = input.read()
        decompressed = h.decompress(text)
        output.write(decompressed)
localtime = time.asctime(time.localtime(time.time()))
print("Decompression Finished: " + localtime)

verify()
