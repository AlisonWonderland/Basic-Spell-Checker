#!/usr/bin/env python3

from nltk import bigrams, trigrams
import nltk.tokenize
from nltk.corpus import brown
# nltk.download('brown')
from collections import Counter, defaultdict
import enchant
import sys

import json

def brownWordOccurences():
    wordOccurences = defaultdict(lambda: 0)

    for fileid in brown.fileids():
        wordList = brown.words(fileid)
        for word in wordList:
            wordOccurences[word.lower()] += 1
    
    return wordOccurences

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
                # print('new:', newWord)

        
    # Remove letter(s)
    for i in range(len(word)):
        newWord = word[:i] + word[(i+1):]
        if newWord == "":
            continue
        if dictionary.check(newWord):
                # maybe calculate the distance here
                validGeneratedWords.append(newWord)
                # print('Removed letter:', newWord)

    # subsitute a letter
    for letter in alphabet:
        for i in range(len(word)):
            newWord = word[:i] + letter + word[(i+1):]
            if dictionary.check(newWord):
                    # maybe calculate the distance here
                    validGeneratedWords.append(newWord)
                    # print('Subsituted letter:', newWord)

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
                    # print('Adjacent letter:', newWord)

    return validGeneratedWords

def giveSuggestions(wordHistory, newWords, model, wordOccurences):
    # Case where one of the first two words are spelled incorrectly.
    # Can't use model so use wordOccurences in brown courpuses
    mostOccuringWord = ""
    maxOccurences = 0
    if len(wordHistory) < 2:
        for word in newWords:
            numOccurences = wordOccurences.get(word.lower(), 0)
            if numOccurences:
                if(numOccurences > maxOccurences):
                    mostOccuringWord = word
                    maxOccurences = numOccurences

    print('Most occuring', mostOccuringWord)

    # print(model[wordHistory[0], wordHistory[1]])


def main():
    # Do a word count for prediction
    wordOccurences = brownWordOccurences()
    # wordOccurences.sort(reverse=True)
    # sys.exit()

    # Model code from:
    # https://www.analyticsvidhya.com/blog/2019/08/comprehensive-guide-language-model-nlp-python-code/
    # Create a placeholder for model
    model = defaultdict(lambda: defaultdict(lambda: 0))

    # Count frequency of co-occurance  
    for sentence in brown.sents():
        for w1, w2, w3 in trigrams(sentence, pad_right=True, pad_left=True):
            model[(w1, w2)][w3] += 1
    
    # Let's transform the counts to probabilities
    for w1_w2 in model:
        total_count = float(sum(model[w1_w2].values()))
        for w3 in model[w1_w2]:
            model[w1_w2][w3] /= total_count


    # readfile
    inputFile = open("sampleInput.txt","r")
    inputText = inputFile.read()
    inputFile.close()

    dictionary = enchant.Dict("en_US")
    inputTokens = nltk.word_tokenize(inputText)

    # editIncorrectWord("cta", d)

    for i in range(len(inputTokens)):
        if not dictionary.check(inputTokens[i]):
            print(inputTokens[i])
            newWords = editIncorrectWord(inputTokens[i], dictionary)
            # if(len(inputTokens[i-2:i]) < 2)
            print("history", inputTokens[i-2:i])
            print("new words", newWords)
            giveSuggestions(inputTokens[i-2:i], newWords, model, wordOccurences)
    # for word in inputTokens:
    #     if not d.check(word):
    #         # print(word)
    #         newWords = editIncorrectWord(word, dictionary)
    #         giveSuggestions(word, newWords, model, wordOccurences)

    # print(corpusTokens)

main()