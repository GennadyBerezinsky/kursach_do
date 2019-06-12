import random
from collections import OrderedDict, Counter
import time
import sys
import json

start_time = time.time()

lineMatrix = sys.argv[1]
matrixSize = int(sys.argv[2])

startMatrix = [[0 for j in range(matrixSize)] for i in range(matrixSize)]
pheromones = [[0 for j in range(matrixSize)] for i in range(matrixSize)]

for i in range(matrixSize):
    for j in range(matrixSize):
        if i == j:
            startMatrix[i][j] = 1
            pheromones[i][j] = 1
            continue
        if j < i:
            startMatrix[i][j] = startMatrix[j][i]
            pheromones[i][j] = pheromones[j][i]
            continue
        startMatrix[i][j] = int(lineMatrix[0])
        pheromones[i][j] = int(lineMatrix[0])
        lineMatrix = lineMatrix[1:]

r = 0.4

numberOfHeads = len(startMatrix)

def findAnimals(head):
    animalsList = []
    for i in range(numberOfHeads):
        if startMatrix[head][i] == 1 and i != head:
            animalsList.append(i)
    return animalsList

def countNumberOfEdges():
    numberOfEdges = 0
    for i in range(numberOfHeads):
        for j in range(i, numberOfHeads):
            if i != j and startMatrix[i][j] == 1:
                numberOfEdges += 1
    return numberOfEdges * 2

def countEdgesFromHead(head):
    return startMatrix[head].count(1) - 1

def countStartHeadProbability(numberOfEdges):
    startHeadProbability = []
    previousSum = 0
    for i in range(numberOfHeads):
        if i != 0:
            previousSum = startHeadProbability[i - 1]
        startHeadProbability.append(countEdgesFromHead(i) / numberOfEdges + previousSum)
    return [0] + startHeadProbability

def countHeadProbability(head, commonHeads, headSum):
    headProbability = []
    headProbabilityWithoutSum = []
    previousSum = 0

    commonSum = 0
    for i, commonHead in enumerate(commonHeads):
        commonSum += commonHeads.get(i) * pheromones[head][commonHead]

    for i, commonHead in enumerate(commonHeads):
        if i != 0:
            previousSum = headProbability[i - 1]
        headProbability.append(commonHeads.get(commonHead) * pheromones[head][commonHead] / commonSum + previousSum)
        headProbabilityWithoutSum.append(commonHeads.get(commonHead) * pheromones[head][commonHead] / commonSum)
    return [0] + headProbability, headProbabilityWithoutSum

def choosHeadToGo(startHeadProbability, randomWay):
    for count in range(len(startHeadProbability)):
        if count != 0 and randomWay > startHeadProbability[count - 1] and randomWay <= startHeadProbability[count]:
            return count - 1

class OrderedCounter(Counter, OrderedDict): 
    pass

def countCommonHeads(markedList):
    sameAnimals = []
    animals = []
    for i in markedList:
        animals += findAnimals(i)
    if len(markedList) > 1:
        sameAnimals = [k for k, v in OrderedCounter(animals).items() if v > len(markedList) - 1]
    else:
        sameAnimals = animals

    sumsList = []
    sumsSet = {}
    for i in range(numberOfHeads):
        rowSum = 0
        if markedList.count(i) == 1:
            sumsList.append(0)
            sumsSet.update({i: rowSum})
            continue

        noZero = True
        for head in markedList:
            if startMatrix[i][head] == 0:
                noZero = False
                break
        if noZero:
            for head in sameAnimals:
                if startMatrix[i][head] == 1:
                    rowSum += 1
        sumsList.append(rowSum)
        sumsSet.update({i: rowSum})
    return sumsSet, sum(sumsList)
        
numberOfEdges = countNumberOfEdges()

totalAnimalsCount = 0
bestHeadsList = []
for globalCount in range(20):
    markedHeadsList = []
    steps = 0
    commonHeadsSum = 1
    headProbability = countStartHeadProbability(numberOfEdges)
    while commonHeadsSum != 0:
        randomWay = random.random()

        headToGo = choosHeadToGo(headProbability, randomWay)
        markedHeadsList.append(headToGo)

        commonHeads, commonHeadsSum = countCommonHeads(markedHeadsList)
        
        if (commonHeadsSum != 0):
            headProbability, headProbabilityWithoutSum = countHeadProbability(headToGo, commonHeads, commonHeadsSum)

        steps += 1

    for i in range(numberOfHeads):
        for j in range(numberOfHeads):
            if markedHeadsList.count(i) == 1 and markedHeadsList.count(j) == 1 and i != j:
                pheromones[i][j] = pheromones[i][j] + (1 - r) * steps / numberOfHeads
            else:
                pheromones[i][j] = pheromones[i][j] * r

    bestHeadsList = markedHeadsList
    totalAnimalsCount = len(markedHeadsList)

answer = [(time.time() - start_time), totalAnimalsCount, bestHeadsList, startMatrix]
print(json.dumps(answer))