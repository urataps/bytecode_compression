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
    def __init__(self, len):
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}
        self.freq = {}
        self.saved = 0  # number of chars saved
        self.codeLen = len
        self.trie = {}

    # functions for compression

    def make_frequency_dict(self, text):
        for i in range(0, len(text), self.codeLen):
            character = text[i:i+self.codeLen]
            if character not in self.freq:
                self.freq[character] = 1
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
        i = 0
        while i < len(text):
            j = i+2
            seq = ""
            current_seq = text[i:j]
            current_dic = self.trie
            # while there is a new path for the pair
            while current_seq in current_dic and j <= len(text):
                current_dic = current_dic[current_seq]  # go one level deeper
                seq += current_seq
                current_seq = text[j:j+2]
                j += 2
            while seq not in self.codes:
                seq = seq[:-2]
                j -= 2

            encoded_text += self.codes[seq]
            i = j-2
        return encoded_text

    # this one adds extra padding used for byte conversion
    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding)  # las byte is info about padding
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

    def make_tree(self):
        # frequency should be computed before compression
        self.make_heap(self.freq)
        self.merge_nodes()
        self.make_codes()

    def make_trie(self):
        _end = '_end_'
        root = dict()
        for word in self.codes.keys():
            current_dict = root
            for i in range(0, len(word), 2):
                letter = word[i:i+2]
                current_dict = current_dict.setdefault(letter, {})
            current_dict[_end] = _end
        self.trie = root
        return root

    def isOptimal(self):  # if the code does not require more information than the sequence
        for seq in self.codes:
            if len(seq) > 2 and len(seq)*4 <= len(self.codes[seq]):
                return seq
        return True

    def compress(self, text):
        text = text.rstrip()

        self.make_tree()
        encoded_text = self.get_encoded_text(text)
        padded_encoded_text = self.pad_encoded_text(encoded_text)
        b = self.get_byte_array(padded_encoded_text)
        compressed_bytecode = str(binascii.hexlify(b))[2:-1]

        print("Compressed. Total chars saved: ", end="")
        print(len(text) - len(compressed_bytecode))
        self.saved += len(text) - len(compressed_bytecode)

        return compressed_bytecode

    """ functions for decompression: """

    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:]
        encoded_text = padded_encoded_text[:-extra_padding]

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

    def decompress(self, text):
        bit_string = binary(text)
        encoded_text = self.remove_padding(bit_string)
        decompressed_text = self.decode_text(encoded_text)
        return decompressed_text
