

with open("bytecode_decompressed.txt", 'r') as decompr, open("bytecode.txt") as normal:
    first = decompr.read()
    second = normal.read().rstrip()
    print(first == second)
