#!/usr/bin/env python3

import nltk.tokenize
from nltk.corpus import words
import enchant

# Edit incorrect words, words not in the dictionary, to find the most similar words and suggest them.
# Max editDistance of 2 is used in the algorithm
# https://medium.com/@willsentance/how-to-write-your-own-spellchecker-and-autocorrect-algorithm-in-under-80-lines-of-code-6d65d21bb7b6
def editIncorrectWord(word, dictionary):
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", 
                "i", "j", "k", "l", "m", "n", "o", "p",
                "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    validGeneratedWords = []
    generatedWords = []

    # Add a letter(s)
    # insert it in all possible positions
    for letter in alphabet:
        for i in range(len(word)):
            wordList = list(word)
            wordList.insert(i, letter)
            newWord = ''.join(wordList)

            if dictionary.check(newWord):
                # maybe calculate the distance here
                validGeneratedWords.append(newWord)
                print('new:', newWord)

        
    # Remove letter(s)
    for i in range(len(word)):
        newWord = word[:i] + word[(i+1):]
        if newWord == "":
            continue
        if dictionary.check(newWord):
                # maybe calculate the distance here
                validGeneratedWords.append(newWord)
                print('Removed letter:', newWord)

    # subsitute a letter
    for letter in alphabet:
        for i in range(len(word)):
            newWord = word[:i] + letter + word[(i+1):]
            if dictionary.check(newWord):
                    # maybe calculate the distance here
                    validGeneratedWords.append(newWord)
                    print('Subsituted letter:', newWord)

    # switch two adjacent letters.
    for i in range(len(word)-1):
        wordList = list(word)
        temp = wordList[i]
        wordList[i] = wordList[i+1]
        wordList[i+1] = temp
        newWord = ''.join(wordList)

        if dictionary.check(newWord):
                    # maybe calculate the distance here
                    validGeneratedWords.append(newWord)
                    print('Adjacent letter:', newWord)


def main():
    # readfile
    corpusFile = open("sampleInput.txt","r")
    corpus = corpusFile.read()
    corpusFile.close()

    d = enchant.Dict("en_US")
    corpusTokens = nltk.word_tokenize(corpus)

    editIncorrectWord("cta", d)
    # for word in corpusTokens:
    #     if not d.check(word):
    #         # print(word)
    #         editIncorrectWord(word, d)

    # print(corpusTokens)

main()