# coding=utf-8

import os
import math
import time
import csv

def tf(text, corpusList):
    wordTf = getDic(corpusList)
    wordLength = len(text)
    for i in range(wordLength):
        if wordTf.get(text[i]) is not None:
            wordTf[text[i]] += 1
    for key in wordTf:
        if(wordTf[key] != 0):
            wordTf[key] = float(wordTf[key] / wordLength)
    # f = open('output11.txt', 'w', encoding='utf-8')
    # f.write(str(wordTf))
    # time.sleep(5)
    return wordTf

def idf(word, corpusList):
    count = 0
    listLength = len(corpusList)
    for currentCorpus in corpusList:
        if word in set(currentCorpus):
            count += 1
    idf = math.log(float(listLength / count + 1))
    return idf

def tfidf(currentCorpus, corpusList):
    wordTf = tf(currentCorpus, corpusList)
    # print(str(len(wordTf)).encode('utf-8'))
    for word in wordTf:
        Tf = wordTf[word]
        if Tf == 0:
            continue
        Idf = idf(word, corpusList)
        wordTf[word] = Tf * Idf
        # print(str(word + ' ' + currentTfidf[word]))
    
    return wordTf

def getCorpusList(path):
    corpusList = []
    filesList = getFilesList(path)
    filesList.sort()        # for recognize which file is working

    for fileName in filesList:
        fin = open(str(path + "/" + fileName), encoding='utf-8')
        currentFile = fin.read()
        currentFile = currentFile.replace('\n', ' ')
        currentFile = currentFile.split()
        corpusList.append(currentFile)
        fin.close()
    # print(str(corpusList).encode('utf-8'))
    return corpusList, filesList

def getDic(corpusList):
    wordDic = {}
    wordList = []
    # print(str(corpusList[0]))
    corpusCount = len(corpusList)
    for i in range(corpusCount):
        wordList += corpusList[i]
    # for word in range(corpusCount):
    wordList = set(wordList)
    wordListLen = len(wordList)
    wordList = list(wordList)
    for i in range(wordListLen):
        wordDic[wordList[i]] = 0
    return wordDic


def getFilesList(path):
    filesList = os.listdir(path)
    return filesList

def calculate(path):            # tf-idf caculation
    tfidfDic = {}
    corpusList, filesList = getCorpusList(path)
    printFilesList(filesList)
    wordDic = getDic(corpusList)
    # print(str(corpusList).encode('utf-8'))
    corpusLen = len(corpusList)
    for i in range(corpusLen):
        print("file " + str(filesList[i]))
        wordTfidf = tfidf(corpusList[i], corpusList)
        tfidfDic[filesList[i]] = wordTfidf
        # f = open(str(path + '/' + filesList[i] + '_tfidf.txt'), 'w', encoding='utf-8')
        # for currentWord in wordTfidf:
        #     f.write(currentWord + ':' + str(wordTfidf[currentWord]) + '\n')
        # f.close()
    cosList = {}
    disList = {}
    for i in tfidfDic:
        doc1 = tfidfDic['50']
        doc2 = tfidfDic[i]
        print(str('50' + ' ' + i))
        cosList[str(i)] = cos(doc1, doc2)
        disList[str(i)] = euclid(doc1, doc2)
        sameWords(doc1, doc2, i)
        # time.sleep(5)
    sorted(cosList.items(), key = lambda item:item[1], reverse = True)
    sorted(disList.items(), key = lambda item:item[1], reverse = True)
    with open('cosList.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        for k in cosList:
            writer.writerow([k, cosList[k]])
    f.close()
    with open('disList.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        for k in disList:
            writer.writerow([k, disList[k]])
    f.close()



def cos(dic1, dic2):
    numerator = 0.0
    normA = 0.0
    normB = 0.0
    for key in dic1:
        if dic1[key] != 0 and dic2[key] != 0:
            normA += dic1[key] ** 2
            normB += dic2[key] ** 2
            numerator += dic1[key] * dic2[key]
    norm = ((normA * normB) ** 0.5)
    if norm == 0.0:
        return 0
    return numerator / norm

def euclid(dic1, dic2):
    dis = 0.0
    for key in dic1:
        dis += ((dic2[key] - dic1[key]) ** 2) ** 0.5
    return dis


def printFilesList(filesList):
    f = open('filesList.txt', 'w', encoding='utf-8')
    for i in range(len(filesList)):
        f.write(str(filesList[i] + '\n'))

def sameWords(dic1, dic2, fileName):
    sameWordList = []
    allWords = 0
    for key in dic2:
        if dic2[key] != 0:
            allWords += 1
    count = 0
    for key in dic1:
        if dic1[key] != 0 and dic2[key] != 0:
            sameWordList.append(key)
            count += 1
    f = open('sameWordsList.txt', 'a', encoding='utf-8')
    f.write(fileName + ' all words : ' + str(allWords) +', count : ' + str(count) + '\n\n')
    for i in range(len(sameWordList)):
        f.write(str(sameWordList[i]) + '\n')
    return True

if __name__ == "__main__":
    calculate("nyt_corp0")

    