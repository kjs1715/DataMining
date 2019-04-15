# coding=utf-8

import sys
import os
import math
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.datasets import load_iris

data = []
wordList = []
dataList = []
f = open("100_word_vector.txt", 'r', encoding="utf-8")
data = f.read().split('\n')
for i in range(len(data)-1):
    tmp = data[i].split('\t')
    wordList.append(tmp[0])
    dataList.append(tmp[1].split(' '))
dataList = np.array(dataList)

# PCA
pca = PCA(n_components=2)
newData = pca.fit_transform(dataList)
print(newData)

newDataX = []
newDataY = []
for i in range(len(newData)):
    newDataX.append(newData[i][0])
    newDataY.append(newData[i][1])
plt.scatter(newDataX, newDataY)
for i in range(len(newData)):
    plt.text(newDataX[i], newDataY[i], wordList[i], bbox=dict(boxstyle="round"))
plt.xlabel('x')
plt.ylabel('y')
# plt.show()

# tsne
tsne = TSNE(n_components=2)
newData2 = tsne.fit_transform(dataList)
print(newData2)

newDataX2 = []
newDataY2 = []
for i in range(len(newData2)):
    newDataX2.append(newData2[i][0])
    newDataY2.append(newData2[i][1])
plt.scatter(newDataX2, newDataY2)
for i in range(len(newData2)):
    plt.text(newDataX2[i], newDataY2[i], wordList[i], bbox=dict(boxstyle="round"))
plt.xlabel('x')
plt.ylabel('y')
plt.show()
