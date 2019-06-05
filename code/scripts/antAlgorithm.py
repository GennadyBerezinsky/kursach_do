import random
from collections import OrderedDict, Counter

startMatrix = [
    [1, 1, 1, 0, 1],
    [1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1],
    [0, 0, 1, 1, 1],
    [1, 0, 1, 1, 1],
]

pheromones= [
    [0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0],
    [1, 1, 0, 1, 1],
    [0, 0, 1, 0, 1],
    [1, 0, 1, 1, 0],
]

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
        startHeadProbability.append(round(countEdgesFromHead(i) / numberOfEdges + previousSum, 6))
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
        headProbability.append(round(commonHeads.get(commonHead) * pheromones[head][commonHead] / commonSum + previousSum, 4))
        headProbabilityWithoutSum.append(commonHeads.get(commonHead) * pheromones[head][commonHead] / commonSum)
    return [0] + headProbability, headProbabilityWithoutSum

def choosHeadToGo(startHeadProbability, randomWay):
    for count in range(len(startHeadProbability)):
        if count != 0 and randomWay > startHeadProbability[count - 1] and randomWay <= startHeadProbability[count]:
            return count - 1

class OrderedCounter(Counter, OrderedDict): 
    pass

def countCommonHeads(markedList):
    print("Ant way", markedList)
    sameAnimals = []
    animals = []
    for i in markedList:
        animals += findAnimals(i)
    if len(markedList) > 1:
        sameAnimals = [k for k, v in OrderedCounter(animals).items() if v > len(markedList) - 1]
    else:
        sameAnimals = animals
    print("Same animals:", sameAnimals)

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

for globalCount in range(20):
    markedHeadsList = []
    steps = 0
    commonHeadsSum = 1
    headProbability = countStartHeadProbability(numberOfEdges)
    print("The START ways probability:", headProbability)
    while commonHeadsSum != 0:
        print("============ STEP", steps + 1, "===============")
        randomWay = random.random()

        if globalCount == 0 and steps == 0:
            randomWay = 0.57
        if globalCount == 0 and steps == 1:
            randomWay = 0.21
        if globalCount == 0 and steps == 2:
            randomWay = 0.37
        if globalCount == 1 and steps == 0:
            randomWay = 0.7
        if globalCount == 1 and steps == 1:
            randomWay = 0.4

        print("Random number is", randomWay)

        headToGo = choosHeadToGo(headProbability, randomWay)
        print("Choosing head", headToGo, "to go")
        markedHeadsList.append(headToGo)

        commonHeads, commonHeadsSum = countCommonHeads(markedHeadsList)
        print("\nNumber of common heads with each head:", commonHeads)
        
        if (commonHeadsSum != 0):
            headProbability, headProbabilityWithoutSum = countHeadProbability(headToGo, commonHeads, commonHeadsSum)
            print("\nThe ways probability from head", headToGo)
            print(headProbabilityWithoutSum)
            print(headProbability)

        steps += 1

    for i in range(numberOfHeads):
        for j in range(numberOfHeads):
            if markedHeadsList.count(i) == 1 and markedHeadsList.count(j) == 1 and i != j:
                pheromones[i][j] = round(pheromones[i][j] + (1 - r) * steps / numberOfHeads, 4)
            else:
                pheromones[i][j] = round(pheromones[i][j] * r, 4)

    for row in pheromones:
        print(row)