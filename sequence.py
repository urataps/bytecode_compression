# This file calculates the most occuring sequences


def sequences(length, str):
    seq = {}

    for j in range(length-1, len(str)):
        i = j-length-1
        if str[i:j] not in seq:
            seq[str[i:j]] = 1
        else:
            seq[str[i:j]] += 1
    seq = {k: v for k, v in sorted(seq.items(), key=lambda item: item[1], reverse=True) if v > 5}

    return seq


if __name__ == "__main__":
    with open("contracts/0x0a49f544a98b775c2ef10a65d71d083706afa58f.evm", "r") as file:
        bytecode = file.read()
        print(sequences(124, bytecode))
