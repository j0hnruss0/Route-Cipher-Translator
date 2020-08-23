""" Advanced Route Cipher Application that allows messages of varying size and difficulty
    to be encrypted and decrypted, depending on a user's choices and inputs"""

import sys
import random

def set_up():
    """ Main function from where rest of app works, user choices made here"""
    print("\n******Route Cipher Encode/Decoder******")
    dummy_list = ["tset", "teh", 
                  "charlee", "whede",
                  "theyre", "001",
                  "002", "003",
                  "004", "005", "006"]
    code_list = {"east": "w3st",
                 "west": "soutw@rd",
                 "south": "n0rth",
                 "forward": "b@ckward",
                 "up": "d0wn",
                 "increase": "007",
                 "decrease": "008",
                 "succeed": "009",
                 "retreat": "010"}
    message_text = ''
    mode = ''
    message_size = input("How long is your message to be encoded/decoded, 20 words or 42 words? (Enter '20' or '42'): ")
    if message_size == '20' or message_size == '42':
        mode = input("\nDo you want to encode this message or decode it? (Enter '1' to encode, '2' to decode): ")
        if mode == '1' or mode == '2':
            if message_size == '20':
                message_text = input("\nEnter your 20-word message:\n")
            elif message_size == '42':
                message_text = input("\nEnter your 42-word message:\n")
        elif mode != '1' and mode != '2':
            print("Invalid mode input. Please try again", file=sys.stderr)
            set_up()
    elif message_size != '20' and message_size != '42':
            print("Invalid message size input. Please try again", file=sys.stderr)
            set_up()

    if mode == '1':
        encode_main(message_text, message_size, dummy_list, code_list)
    elif mode == '2':
        decode_main(message_text, message_size, dummy_list, code_list)
    
def encode_main(message, size, dummy_list, code_list):
    """Run program to print decrypted text"""
    ROWS = 0
    COLS = 0
    key = ''
    index_key = ''

    if size == '20':
        COLS = 4
        ROWS = 5
        key = '16 12 8 4 0 1 5 9 13 17 18 14 10 6 2 3 7 11 15 19'
    elif size == '42':
        COLS = 6
        ROWS = 7
        key = '36 30 24 18 12 6 0 2 8 14 20 26 32 38 37 31 25 19 13 7 1 5 11 17 23 29 35 41 4 10 16 22 28 34 40 39 33 27 21 15 9 3'

    print("\nPlain Text = {}".format(message))
    print("\nTrying {} columns".format(COLS))
    print("\nTrying {} rows".format(ROWS))
    print("\nTrying key = {}".format(key))

    # elements split into word list
    cipherlist = list(message.split())
    index_key = list(key.split())

    # The following function switches given words with those found in the code_list dictionary
    words_to_codes(cipherlist, code_list)
    validate_matrix(cipherlist, ROWS, COLS, 'encode', dummy_list)
    encodedtext = encrypt(cipherlist, index_key)

    print("Encoded text = {}".format(encodedtext))


def decode_main(message, size, dummy_list, code_list):
    """Run program to print decrypted text"""
    ROWS = 0
    COLS = 0
    key = ''

    if size == '20':
        COLS = 4
        ROWS = 5
        key = '-1 2 -3 4' #neg number read up a column
    elif size == '42':
        COLS = 6
        ROWS = 7
        key = '-1 3 -2 6 5 -4'

    print("\nCipher Text = {}".format(message))
    print("\nTrying {} columns".format(COLS))
    print("\nTrying {} rows".format(ROWS))
    print("\nTrying key = {}".format(key))
    
    # elements split into word list, then code words substitute regular words  
    cipherlist = list(message.split())
    codes_to_words(cipherlist, code_list)

    # functions that define decryption/encryption/and validation processes 
    validate_matrix(cipherlist, ROWS, COLS, 'decode', dummy_list)
    key_int = key_convert(key, COLS)
    translation_matrix = build_matrix(key_int, cipherlist, ROWS, COLS)
    plaintext = decrypt(translation_matrix, ROWS, dummy_list)

    print("Plain text = {}".format(plaintext))

def validate_matrix(cipherlist, ROWS, COLS, valid_mode, dummy_list):
    """Checks that user input is the proper length versus message length"""
    factors = []
    cipher_len = len(cipherlist)
    for i in range(2, cipher_len): # 1-column ciphers excluded
        if cipher_len % i == 0:
            factors.append(i)
    print("\nLength of cipher = {}".format(cipher_len))
    print("\nAcceptable row/columns values include: {}".format(factors))
    print()
    if ROWS * COLS != cipher_len and valid_mode == 'decode':
        if ROWS * COLS > cipher_len:
            print("Your message is {} word(s) too short", file=sys.stderr)
        elif ROWS * COLS < cipher_len:
            print("Your message is {} word(s) too long", file=sys.stderr)
        print("\nERROR: Input does meet proper message length. Terminating...", 
                file=sys.stderr)
        sys.exit(1)
    elif ROWS * COLS != cipher_len and valid_mode == 'encode':
        if ROWS * COLS > cipher_len:
            dummy_no = (ROWS * COLS) - cipher_len
            for i in range(dummy_no):
                cipherlist.append(random.choice(dummy_list))
        elif ROWS * COLS < cipher_len:
            print("Your message is {} word(s) too long", file=sys.stderr)
            print("\nERROR: Input does meet proper message length. Terminating...", 
                file=sys.stderr)

def key_convert(key, COLS):
    """key converts into list of integers and validity is checked"""
    key_int = [int(i) for i in key.split()]
    key_low = min(key_int)
    key_high = max(key_int)
    if (len(key_int) != COLS or 
        key_low < -COLS or 
        key_high > COLS or 
        0 in key_int):
        print("ERROR: Problem with given key. Terminating...", file=sys.stderr)
        sys.exit(1)
    else:
        return key_int

def build_matrix(key_int, cipherlist, ROWS, COLS):
    """Rearranges the encrypted phrase by adding cipherlist elements into the translation_matrix"""
    translation_matrix = [None] * COLS
    start = 0
    stop = ROWS
    for k in key_int:
        if k < 0: # Bottom-to-top column reading
            col_items = cipherlist[start:stop]
        elif k > 0: # Top-to-bottom column reading
            col_items = list((reversed(cipherlist[start:stop])))
        translation_matrix[abs(k) - 1] = col_items
        start += ROWS
        stop += ROWS

    return translation_matrix

def words_to_codes(cipherlist, code_list):
    """Swaps uncoded words from message with coded words from code_list dictionary"""
    for word in cipherlist:
        if word in code_list.keys():
            for code_word in code_list.keys():
                if code_word == word:
                    cipherlist[cipherlist.index(word)] = code_list[code_word]
    
    return cipherlist

def codes_to_words(cipherlist, code_list):
    """If there are coded words in the encrypted message, this function swaps the original
       words back in for the decrypted message"""
    for word in cipherlist:
        if word in code_list.values():
            for code_word in code_list.items():
                if code_word[1] == word:
                    cipherlist[cipherlist.index(word)] = code_word[0]
        
    return cipherlist


def decrypt(translation_matrix, ROWS, dummy_list):
    """Loop through the nested translation_matrix lists and popping off the
       last items and adding to a decrypted string"""
    
    plaintext = ''

    for all in range(ROWS):
        for matrix_col in translation_matrix:
            word = str(matrix_col.pop())
            if word not in dummy_list:
                plaintext += word + ' '
    return plaintext

def encrypt(cipherlist, index_key):
    encodedtext = ''
    for i in index_key:
        encodedtext += cipherlist[int(i)] + ' '

    return encodedtext

if __name__ == '__main__':
    set_up()