#!/usr/bin/env python3
# import nltk.tokenize
import re
import sys

def extractNgrams(textList, n):
    ngrams = []
    
    for i in range(len(textList)-n+1):
        ngramWords = textList[i:i+n]
        ngram=""
        for j in range(n):
            if j != n - 1:
                ngram += ngramWords[j] + " "
            else:
                ngram += ngramWords[j]
        ngrams.append(ngram)

inputFile = open("sampleInput.txt","r")
inputText = inputFile.read()
inputFile.close()

# Clean up text so there is no punction except for '
inputText = re.sub(r'[^A-Za-z0-9 \']', '', inputText)
cleanedText = inputText.split(' ')

extractNgrams(cleanedText, int(sys.argv[1]))

# inputTokens = nltk.word_tokenize(inputText)