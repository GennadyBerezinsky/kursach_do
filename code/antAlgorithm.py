import random

startMatrix = [
    [1, 1, 1, 0, 1],
    [1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1],
    [0, 0, 1, 1, 1],
    [1, 0, 1, 1, 1]
]

pheromones= [
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
    previousSum = 0
    for i, commonHead in enumerate(commonHeads):
        if i != 0:
            previousSum = headProbability[i - 1]
        headProbability.append(round(commonHeads.get(commonHead) * pheromones[head][commonHead] / headSum * pheromones[head][commonHead] + previousSum, 6))
    return [0] + headProbability

def choosHeadToGo(startHeadProbability, randomWay):
    for count in range(len(startHeadProbability)):
        if count != 0 and randomWay > startHeadProbability[count - 1] and randomWay <= startHeadProbability[count]:
            return count - 1

def countCommonHeads(head):
    commonHeadsList = {}
    animalsList = findAnimals(head)
    commonHeadsSum = 0
    for i in range(numberOfHeads):
        commonSum = 0
        for j in range(numberOfHeads):
            if i != j and startMatrix[i][j] == 1 and animalsList.count(i) != 0 and j != head:
                commonSum += 1
        commonHeadsList.update({i: commonSum})
        commonHeadsSum += commonSum
    return commonHeadsList, commonHeadsSum
        
numberOfEdges = countNumberOfEdges()
headProbability = countStartHeadProbability(numberOfEdges)

print("The ways probability:", headProbability)

for i in range(2):
    print("============ STEP", i + 1, "===============")
    randomWay = random.random()
    # Delete later
    if i == 0:
        randomWay = 0.57
    if i == 1:
        randomWay = 0.21
    print("Random number is", randomWay)

    headToGo = choosHeadToGo(headProbability, randomWay)
    print("Choosing head", headToGo, "to go")

    commonHeads = countCommonHeads(headToGo)
    print("\nNumber of common heads with each head:", commonHeads)

    headProbability = countHeadProbability(headToGo, commonHeads[0], commonHeads[1])
    print("\nThe ways probability from head", headToGo)
    print(headProbability)
