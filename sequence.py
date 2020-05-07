# This file calculates the most occuring sequences
import os

dict = {}
for filename in os.listdir("contracts"):
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


dict = {k: (v*len(k))//2 for k, v in dict.items() if v > 20 and len(k) > 2}

RedSeq = set()  # register sequences that do not occur independently
Seq = list(dict.keys())  # all sequences

for i in range(len(Seq)):
    for j in range(i+1, len(Seq)):
        s1 = Seq[i]
        s2 = Seq[j]
        if s1 in s2 and dict[s1] <= dict[s2]:
            RedSeq.add(s1)

for red in RedSeq:
    del dict[red]

dict = {k: (2*v)//len(k) for k, v in dict.items()}


def isAtom(s1, Seqs):
    for s2 in Seqs:
        if s1 != s2 and s1 in s2:
            return False
    return True


def independent(dict):
    Seq = list(dict.keys())
    Atoms = [x for x in Seq if isAtom(x, Seq)]
    NotAtoms = [x for x in Seq if not isAtom(x, Seq)]
    for notAtom in NotAtoms:
        for atom in Atoms:
            if notAtom in atom:
                dict[notAtom] = dict[notAtom] - atom.count(notAtom) * dict[atom]

    return {k: v for k, v in sorted(dict.items(), key=lambda item: item[1]) if len(k) == 2 or v > 1}
