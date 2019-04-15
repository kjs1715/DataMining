# coding=utf-8

import os
import math
import time
import csv

def getFilesList(path):
    filesList = os.listdir(path)
    return filesList

def getCorpusList(path):
    corpusDocList = []          # by docs
    corpusList = []             # by words
    filesList = getFilesList(path)
    filesList.sort()

    for fileName in filesList:
        fin = open(str(path + "/" + fileName), encoding='utf-8')
        currentFile = fin.read()
        currentFile = currentFile.replace('\n', ' ')
        currentFile = currentFile.split()
        corpusList += currentFile
        corpusDocList.append(currentFile)
        fin.close()
    corpusList = set(corpusList)
    corpusList = list(corpusList)
    return corpusDocList, filesList, corpusList

def getDic(corpusDocList, corpusList):
    print('wordDic preparing..')
    wordDic = {}
    wordCount = len(corpusList)
    docCount = len(corpusDocList)
    for word in range(wordCount):
        wordDocSet = set()
        for i in range(docCount):
            if corpusList[word] in corpusDocList[i]:
                wordDocSet.add(i)
        wordDic[corpusList[word]] = wordDocSet
    return wordDic

def calculate(path):
    corpusDocList, filesList, corpusList = getCorpusList(path)
    wordDic = getDic(corpusDocList, corpusList)
    print(str(wordDic).encode('utf-8'))
    wordcount = len(corpusList)
    matrix = [[0] * 1 for i in range(wordcount)]
    # print(matrix)

    for i in range(len(corpusList)):
        for j in range(len(corpusList)):
            if i > j:
                temp = wordDic[corpusList[i]] & wordDic[corpusList[j]]
                if j != 0:
                    matrix[i].append(len(temp))
                else:
                    matrix[i][j] = len(temp)
            elif i == j:
                if j != 0:
                    matrix[i].append(0)
                else:
                    matrix[i][j] = 0
            print('(' + str(i) + ', ' + str(j) + ') -> ' + str(matrix[i][j]))
                # print(str(corpusList[i]) + ' ' + str(corpusList[j]))

    for i in range(len(corpusList)):
        for j in range(len(corpusList)):
            if j > i:
                matrix[i].append(matrix[j][i])
    with open('matrix.txt', 'w', encoding='utf-8') as f:
        for i in range(len(corpusList)):
            f.write(str(matrix[i]) + '\n')
    f.close()
    cosList = {}
    eucList= {}
    word1 = 25
    print('matrix complete...')
    for word2 in range(len(corpusList)):
        print('calculating ' + str(word2))
        cosList[corpusList[word2]] = cos(word1, word2, matrix, len(corpusList))
        eucList[corpusList[word2]] = euclid(word1, word2, matrix, len(corpusList))
    writeCsv(cosList, eucList, corpusList[25])
    return True

def cos(word1, word2, matrix, length):
    numerator = 0.0
    normA = 0.0
    normB = 0.0
    for i in range(length):
        normA += matrix[word1][i] ** 2
        normB += matrix[word2][i] ** 2
        numerator += matrix[word1][i] * matrix[word2][i]
    norm = ((normA * normB) ** 0.5)
    if norm == 0.0:
        return 0
    return numerator / norm

def euclid(word1, word2, matrix, length):
    dis = 0.0
    for i in range(length):
        dis += ((matrix[word1][i] - matrix[word2][i]) ** 2) ** 0.5
    return dis

def writeCsv(cosList, eucList, targetWord):
    with open('cosList2.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        for k in cosList:
            writer.writerow([k, cosList[k]])
        writer.writerow([targetWord])
    f.close()
    with open('disList2.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        for k in eucList:
            writer.writerow([k, eucList[k]])
        writer.writerow([targetWord])
    f.close()

if __name__ == "__main__":
    calculate('nyt_corp0')
