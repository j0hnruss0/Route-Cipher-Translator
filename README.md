# Route-Cipher-Translator
A translator app for message ciphers used during the American Civil War. Based on content from Impractical Python Projects
by Lee Vaughan, one of the challenge projects in Chapter 4

Users can choose wether to decode or code a route cipher encrypted message,
based on the list of keys [-1, 3, -2, 6, 5, -4] for large 42-word ciphers 
and [-1, 2, -3, 4] for smaller 20-word ciphers. If the input given for encoding is less
than the expected value, dummy words from a dummy_list will be put in instead. They will
be automatically removed when decoding the message

Route ciphers work by rearranging the places of words in a phrase according
to their ordr (0 = 1st word, 1 = 2nd word, etc. Positioning mimics indexing in Python),
plus number of rows and columns to correspond to how many words are present
(16-word phrase: 4x4 grid, 42 words: 6x7 grid)

 0  1  2  3  4  5      To create the cipher, the number of words present, starting 
 6  7  8  9 10 11      with 0, are arranged in a gird like seen to the left, and the 
12 13 14 15 16 17      key is used to find a column and the word are placed from bottom
18 19 20 21 22 23      to top (if the key is negative) or top to bottom (if the key is
24 25 26 27 28 29      positive). using the order of keys in the list, the words in the
30 31 32 33 34 35      original order are rearranged to create a encrypted message. You
36 37 38 39 40 41      can use the same grid matrix to decrypt a message to, as long as
                       the same key is used with the same grid as the message was encrypted

The encoded/decoded message will be provided in the end

Additionally, if a given uncoded message has words found in the code_list, the values
of those key words will be put in the encoded message for additionaly secrecy. Conversely,
when decoding a message, words swapped with coded words will be converted back to the
intended word in the original message
