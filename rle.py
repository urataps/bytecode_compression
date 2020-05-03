# This file implements optimized run-length encoding
# AABBBBCCC -> AAB4*CCC


import os


def encode(message):
    encoded_message = ""
    i = 0

    while (i <= len(message)-1):
        count = 1
        ch = message[i]
        j = i
        while (j < len(message)-1):
            if (message[j] == message[j+1]):
                count = count+1
                j = j+1
            else:
                break
        if count > 3:
            encoded_message += ch + '*' * len(str(count)) + str(count)
        else:
            encoded_message += ch * count
        i = j+1
    return encoded_message


def decode(message):
    decoded_message = ""
    i = 0
    while (i <= len(message)-1):
        if message[i] == '*':
            count = 1  # counts the number of asterixs
            j = i
            while (j < len(message)-1):
                if (message[j] == message[j+1]):
                    count += 1
                    j += 1
                else:
                    break
            j += 1  # puts j at the start of count
            times = int(message[j:j+count])
            ch = message[i-1] * (times-1)
            i = j+count
        else:
            ch = message[i]
            i += 1
        decoded_message += ch
    return decoded_message


total_len = 0
total_cmp = 0
for filename in os.listdir("contracts"):
    with open('contracts/' + filename, 'r') as file:
        text = file.read()
        total_len += len(text)
        total_cmp += len(encode(text))

saved = total_len - total_cmp

print("Total saved: ", saved)
print(saved*100/total_len, ' %')
