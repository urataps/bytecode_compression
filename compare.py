# This file verifies if the no information was lost after decompression
import os


def verify():
    for filename in os.listdir("contracts"):
        with open("contracts/" + filename, 'r') as normal, open("hybriddecompressed_contracts/" + filename, "r") as decompressed:
            first = decompressed.read().rstrip()
            second = normal.read().rstrip()
            if first != second:
                print(filename + " does not correspond")
    print("Decompressed files correspond with acutal ones.")
