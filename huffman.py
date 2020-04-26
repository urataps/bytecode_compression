# This file implements the huffman encoding

import binascii
import heapq
import os


# function to convert from hex to binary string
def binary(x):
    return "".join(reversed([i+j for i, j in zip(*[["{0:04b}".format(int(c, 16)) for c in reversed("0"+x)][n::2] for n in [1, 0]])]))


class HeapNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        if(other == None):
            return -1
        if(not isinstance(other, HeapNode)):
            return -1
        return self.freq < other.freq


class HuffmanCoding:
    def __init__(self):
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}
        self.freq = {}
        self.saved = 0  # number of chars saved

    # functions for compression:
    def make_frequency_dict(self, text):
        for character in text:
            if character not in self.freq:
                self.freq[character] = 0
            self.freq[character] += 1
        return self.freq

    # this function puts every leaf node in the heap
    def make_heap(self, frequency):
        for key in frequency:
            node = HeapNode(key, frequency[key])
            heapq.heappush(self.heap, node)

    # this function takes 2 nodes with min frequency and merges them and inserts into heap
    def merge_nodes(self):
        while(len(self.heap) > 1):
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)

    # this function computes the codeword for each character stored in self.codes
    def make_codes_helper(self, root, current_code):
        if(root == None):
            return

        if(root.char != None):
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    # actually this function is called
    def make_codes(self):
        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root, current_code)

    # this function encodes the text
    def get_encoded_text(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text

    # this one adds extra padding used for byte conversion
    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    # this one converts encoded text to bytes
    def get_byte_array(self, padded_encoded_text):
        if(len(padded_encoded_text) % 8 != 0):
            print("Encoded text not padded properly")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            b.append(int(byte, 2))
        return b

    def compress(self, path):
        filename, file_extension = os.path.splitext(path)
        output_path = "compressed_" + filename + "_cmp" + file_extension

        with open(path, 'r') as file, open(output_path, 'w') as output:
            text = file.read()
            text = text.rstrip()

            # frequency should be computed before compression
            self.make_heap(self.freq)
            self.merge_nodes()
            self.make_codes()
            encoded_text = self.get_encoded_text(text)
            padded_encoded_text = self.pad_encoded_text(encoded_text)

            b = self.get_byte_array(padded_encoded_text)
            compressed_bytecode = str(binascii.hexlify(b))[2:-1]
            output.write(compressed_bytecode)
        print("Compressed. Total chars saved: ", end="")
        print(len(text) - len(compressed_bytecode))
        self.saved += len(text) - len(compressed_bytecode)
        return output_path

    """ functions for decompression: """

    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:]
        encoded_text = padded_encoded_text[:-1*extra_padding]

        return encoded_text

    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if(current_code in self.reverse_mapping):
                character = self.reverse_mapping[current_code]
                decoded_text += character
                current_code = ""

        return decoded_text

    def decompress(self, input_path):
        filename, file_extension = os.path.splitext(input_path)
        output_path = filename + "_dcmp" + file_extension

        with open(input_path, 'r') as input, open(output_path, 'w') as output:
            text = input.read()
            bit_string = binary(text)
            encoded_text = self.remove_padding(bit_string)
            decompressed_text = self.decode_text(encoded_text)
            output.write(decompressed_text)

        print("Decompressed")
        return output_path
