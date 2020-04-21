#!/usr/bin/env python3

import nltk.tokenize
from nltk.corpus import words
import enchant

# Edit incorrect words, words not in the dictionary, to find the most similar words and suggest them.
# Max editDistance of 2 is used in the algorithm
# https://medium.com/@willsentance/how-to-write-your-own-spellchecker-and-autocorrect-algorithm-in-under-80-lines-of-code-6d65d21bb7b6
def editIncorrectWord(word):
    # Add a letter(s)

    # Remove letter(s)

    # subsitute a letter 

    # switch two adjacent letters.


def main():
    # readfile
    corpusFile = open("sampleInput.txt","r")
    corpus = corpusFile.read()
    corpusFile.close()

    d = enchant.Dict("en_US")
    corpusTokens = nltk.word_tokenize(corpus)

    for word in corpusTokens:
        if not d.check(word):
            print(word)

    print(corpusTokens)

main()