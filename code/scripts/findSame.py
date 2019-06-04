from collections import OrderedDict, Counter

startMatrix = [
    [1, 1, 1, 0, 1],
    [1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1],
    [0, 0, 1, 1, 1],
    [1, 0, 1, 1, 1]
]

numberOfHeads = len(startMatrix)

def findAnimals(head):
    animalsList = []
    for i in range(numberOfHeads):
        if startMatrix[head][i] == 1 and i != head:
            animalsList.append(i)
    return animalsList

class OrderedCounter(Counter, OrderedDict): 
    pass

def countCommonHeads(markedList):
    sameAnimals = []
    animals = []
    for i in markedList:
        print(findAnimals(i))
        animals += findAnimals(i)
    if len(markedList) > 1:
        sameAnimals = [k for k, v in OrderedCounter(animals).items() if v > len(markedList) - 1]
    else:
        sameAnimals = animals
    print("Same animals:", sameAnimals)

    sumsList = []
    for i in range(numberOfHeads):
        rowSum = 0
        if markedList.count(i) == 1:
            sumsList.append(0)
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
    
    print(sumsList, sum(sumsList))
                
data = countCommonHeads([2, 0])

