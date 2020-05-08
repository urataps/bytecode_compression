# This file calculates the most occuring sequences
import os
from tqdm import tqdm

dict = {}
for filename in tqdm(os.listdir("contracts")):
    with open("contracts/" + filename, "r") as file:
        text = file.read().rstrip()

    w = ''

    for i in range(0, len(text), 2):
        c = text[i:i+2]
        wc = w+c

        if wc in dict:
            dict[wc] += 1
            w = wc
        else:
            dict[wc] = 1
            w = c


dict = {k: (v*len(k))//2 for k, v in dict.items() if v > 700 and len(k) > 2}

RedSeq = set()  # register sequences that do not occur independently
Seq = list(dict.keys())  # all sequences

for i in tqdm(range(len(Seq))):
    for j in range(i+1, len(Seq)):
        s1 = Seq[i]
        s2 = Seq[j]
        if s1 in s2 and dict[s1] <= dict[s2]:
            RedSeq.add(s1)

for red in tqdm(RedSeq):
    del dict[red]

dict = {k: (2*v)//len(k) for k, v in dict.items()}
