from string import ascii_lowercase
import pandas as pd
import string
from collections import Counter

ENGLISH_FREQ = {'e': 12.02, 't': 9.10, 'a': 8.12, 'o': 7.68, 'i': 7.31, 'n': 6.95,
                's': 6.28, 'r': 6.02, 'h': 5.92, 'd': 4.32, 'l': 3.98, 'u': 2.88,
                'c': 2.71, 'm': 2.61, 'f': 2.30, 'y': 2.11, 'w': 2.09, 'g': 2.03,
                'p': 1.82, 'b': 1.49, 'v': 1.11, 'k': 0.69, 'x': 0.17, 'q': 0.11,
                'j': 0.10, 'z': 0.07}


def freq_count(ct):
    freq = {l: 0 for l in ascii_lowercase}
    ct = ct.lower()
    for l in ct:
        if l in freq:
            freq[l] += 1
    freq = sorted(freq.items(), key=lambda x: x[0])
    df = pd.DataFrame(freq, columns=['Character', 'Frequency'])
    return df

# # without zero frequency letters
# def freq_count(ct):
#     freq = {l: 0 for l in ascii_lowercase}
#     ct = ct.lower()
#     for l in ct:
#         if l in freq:
#             freq[l] += 1
#     freq = {k: v for k, v in freq.items() if v != 0}
#     freq = sorted(freq.items(), key=lambda x: x[0])
#     df = pd.DataFrame(freq, columns=['Character', 'Frequency'])
#     return df


# def calculate_likelihood(plaintext):
#     frequency = freq_count(plaintext)
#     total_chars = sum([f[1] for f in frequency])
#     likelihood = 0
#     for char, freq in frequency:
#         if char in ENGLISH_FREQ:
#             print((100 * freq / total_chars))
#             likelihood += abs((100 * freq / total_chars) - ENGLISH_FREQ[char])
#     return max(0, 100 - likelihood)  

def letter_frequency(text):
    cleaned_text = ''.join(char.lower() for char in text if char.isalpha())
    frequencies = Counter(cleaned_text)
    total_letters = sum(frequencies.values())
    
    for char in string.ascii_lowercase:
        if char not in frequencies:
            frequencies[char] = 0
    
    distribution = {letter: 100 * count / total_letters for letter, count in frequencies.items()}
    return distribution


def ct_likelihood(text):
    dist1 = letter_frequency(text)
    letters = set(ENGLISH_FREQ.keys()) | set(dist1.keys())
    mse = sum((ENGLISH_FREQ.get(letter, 0) - dist1.get(letter, 0))**2 for letter in letters) / len(letters)
    mse = 100 - mse
    return round(100*((mse - 65) / (100 - 65)), 2)


def detect_shift(freq):
    return abs(ord('e') - ord(freq[0][1]))

def encryptCeaser(message, shift):
    ct = ""
    message = message.lower()
    for l in message:
        if l not in ascii_lowercase:
            ct += l
            continue
        c = ord(l) - ord('a')
        c = (c + shift) % 26
        ct += ascii_lowercase[c]
    return ct

def decryptCeaser(ct, shift):
    message = ""
    ct = ct.lower()
    for l in ct:
        if l not in ascii_lowercase:
            message += l
            continue
        c = ord(l) - ord('a')
        c = (c - shift) % 26
        message += ascii_lowercase[c]
    if len(message) < 30:
        like = "Message too short"
    else:
        like = ct_likelihood(message)
    return message, like


if __name__ == "__main__":
    message = "Hello World"
    print(message)
    # ct = encryptCeaser(message, 16)
    # print(ct)
    print(freq_count(message))