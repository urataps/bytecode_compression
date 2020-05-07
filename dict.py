import os

dict = {}

for i in range(256):
    h = hex(i)[2:]
    if len(h) == 1:
        h = '0' + h
    dict[h] = 0

redundant = {}
filename = '0x0a49f544a98b775c2ef10a65d71d083706afa58f.evm'

with open("contracts/" + filename, "r") as file:
    text = file.read().rstrip()


w = ''
for i in range(0, len(text), 2):
    c = text[i:i+2]
    wc = w+c

    if wc in dict:
        dict[wc] += 1
        if w not in redundant and len(w) != 0:
            redundant[w] = {wc}
        elif w in redundant and len(w) != 0:
            redundant[w].add(wc)
        w = wc
    else:
        dict[wc] = 1
        w = c
