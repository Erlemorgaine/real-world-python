import sys
import os
import random

# Default dict will supply a default value when adding a key without a value
# (contrary for a normal dictionary, that will throw an error)
# Counter is a dictionary for storing counts of elements, in which the elements are the key and the counts are the value
from collections import defaultdict, Counter

def load_file(infile):
    # Read and return a text file as a string of lowercase characters
    with open(infile, encoding='utf-8', errors='ignore') as f:
        loaded_string = f.read().lower()
    return loaded_string

def make_dict(text, shift):
    # Return dictionary of characters and shifted indexes
    char_dict = defaultdict(list)
    for index, char in enumerate(text):
        # So in the end we get a key with a list of shifted indices
        char_dict[char].append(index + shift)
    return char_dict

def encrypt(message, char_dict):
    # Return list of shifted indices representing characters in a message
    encrypted = []

    for char in message.lower():
        if len(char_dict[char]) > 1:
            index = random.choice(char_dict[char])
        elif len(char_dict[char]) == 1:
            index = char_dict[char][0]
        elif len(char_dict[char]) == 0:
            print('\nCharacter does not exist in dictionary\n', file=sys.stderr)
            continue # Skip appending this index, we will see later in the quality check that the character
                     # is missing in the message
        encrypted.append(index)
    return encrypted

def decrypt(ciphertext, booktext, shift):
    # Decrypt ciphertext and return plain string
    plaintext = ''
    # The idea is that the user copypastes a list if indices as input (with or without square brackets)
    indices = [s.replace(',', '').replace('[', '').replace(']', '') for s in ciphertext.split()]
    for i in indices:
        plaintext += booktext[int(i) - shift]
    return plaintext

def check_for_fail(ciphertext):
    # Return true of ciphertext contains any duplicates.
    # Use counter to check if there are duplicate items in the cipher list
    check = [k for k, v in Counter(ciphertext).items() if v > 1]
    if len(check) > 0:
        return True

def main():
    message = input('\nEnter message to encrypt (plaintext) or decrypt (ciphertext)\n')
    process = input('\nEnter encrypt or decrypt\n')
    
    while process not in ('encrypt', 'decrypt'):
        process = input('\nInvalid process. Enter encrypt or decrypt\n')

    # Shift: max = days in leap year
    shift = int(input("\nShift value (1-366):\n"))
    while not 1 <= shift <= 366:
        shift = int(input("\nInvalid input. Shift value (1-366):\n"))

    # This is the book we'll use for the encryption
    infile = input("\nEnter filename with extension\n")
    if not os.path.exists(infile):
        # file=sys.stderr colors the printed message red
        print('\nFile not found, ending program.\n', file=sys.stderr)
        sys.exit(1)

    booktext = load_file(infile)
    char_dict = make_dict(booktext, shift)

    if process == 'encrypt':
        ciphertext = encrypt(message, char_dict)

        # Here we start a process of quality control to ensure the message has been encrypted correctly
        if check_for_fail(ciphertext):
            print('\nProblem finding unique keys', file=sys.stderr)
            print('\nTry again, change message, or change codebook.\n')
            sys.exit()
        
        # This is just to check which characters and how many there are in the book, 
        # to get an idea of which characters you can use in the message (you should use characters
        # with a high frequency to prevent duplication)
        print('\nCharacter and number of occurences in character dictionary:\n')
        # This format prints three columns with headers
        print('{: >10}{: >10}{: >10}'.format('Character', 'Unicode', 'Count'))

        for key in sorted(char_dict.keys()):
            # repr() allows you to print all useful information about the key, e.g. it would print \n (newline)
            # [1:-1] eliminates quotes on the sides of the string returned by repr()
            # We want to show the unicode value to check for strange things happening in text file
            print('{: >10}{: >10}{: >10}'.format(repr(key)[1:-1], str(ord(key)), len(char_dict[key])))

        print('\nNumber of distinct characters in book: {}\n'.format(len(char_dict)))
        print('\nTotal number of characters in book: {:,}\n'.format(len(booktext)))

        print('\nEncrypted ciphertext = \n{}\n'.format(ciphertext))
        print('\nDecrypted plaintext = \n')

        for charCode in ciphertext:
            print(booktext[charCode - shift], end='', flush=True)


    elif process == 'decrypt':
        decrypted_message = decrypt(message, booktext, shift)
        print('\nDecrypted text: \n{}'.format(decrypted_message))

# Boilerplate code to call program as a module or standalone
if __name__ == '__main__':
    main()