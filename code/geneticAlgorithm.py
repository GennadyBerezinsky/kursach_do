import random

def getRandomPopulation(stringLength):
    letters = "01"
    return ''.join(random.choice(letters) for i in range(stringLength))

def checkAnimals(matrix, animalOneNumber, animalTwoNumber):
    return matrix[animalOneNumber][animalTwoNumber] == 1

def checkIfSatisfy(matrix, item):
    animalNumbers = []
    for count, element in enumerate(item, start = 0):
        if (element == '1'):
            animalNumbers.append(count)
    for i in range(len(animalNumbers)):
        for j in range(len(animalNumbers)):
            if checkAnimals(matrix, animalNumbers[i], animalNumbers[j]) == False:
                return False
    
    return True

def countAnimals(item):
    count = 0
    for letter in item:
        if letter == '1':
            count += 1
    return count

def printPopulations(count, startMatrix, populationItem):
    print(str(count) + ". " 
    + populationItem 
    + " C("+ str(count) +") = " 
    + str(countAnimals(populationItem))
    + " " + str(checkIfSatisfy(startMatrix, populationItem)))

def findMaxFromPopulations(firstGroup, secondGroup):
    maxNumber = 0
    maxFirstName = ''
    for element in firstGroup:
        if countAnimals(element) > maxNumber:
            maxNumber = countAnimals(element)
            maxFirstName = element

    maxNumber = 0
    maxSecondName = ''
    for element in secondGroup:
        if countAnimals(element) > maxNumber:
            maxNumber = countAnimals(element)
            maxSecondName = element

    return [maxFirstName, maxSecondName]

def crossingOver(parentsList):
    firstBlockSize = int(len(parentsList[0])/2)
    secondBlockSize = len(parentsList[0]) - firstBlockSize

    firstFirstPart = parentsList[0][:firstBlockSize]
    firstSecondPart = parentsList[0][secondBlockSize:]
    secondFirstPart = parentsList[1][:firstBlockSize]
    secondSecondPart = parentsList[1][secondBlockSize:]

    parentsList[0] = firstFirstPart + secondSecondPart
    parentsList[1] = secondFirstPart + firstSecondPart

    return parentsList

startMatrix = [
    [1, 1, 1, 0, 1, 0],
    [1, 1, 1, 0, 1, 0],
    [1, 1, 1, 0, 1, 1],
    [0, 0, 0, 1, 1, 0],
    [1, 1, 1, 1, 1, 1],
    [0, 0, 1, 0, 1, 1]
]

matrixLen = len(startMatrix)

populationList = []

for i in range(16):
    randomPopulation = getRandomPopulation(matrixLen)
    if populationList.count(randomPopulation) == 0:
        populationList.append(randomPopulation)

# Delete later
populationList = ['100101', '011001', '011000', '010101', '010010', '001011', '110001', '111000']

print("Generated population:")
whatToDelete = []
for count, populationItem in enumerate(populationList, start = 0):
    printPopulations(count + 1, startMatrix, populationItem)
    if checkIfSatisfy(startMatrix, populationItem) == False:
        whatToDelete.append(populationItem)
    
for element in whatToDelete:
    populationList.remove(element)

print("\nCleaned population:")
for count, populationItem in enumerate(populationList, start = 0):
    printPopulations(count + 1, startMatrix, populationItem)

numberOfCandidatesAtFirstGroup = int(len(populationList) / 2)
numberOfCandidatesAtSecondGroup = len(populationList) - numberOfCandidatesAtFirstGroup

firstGroup = []
secondGroup = []

randomList = populationList
while len(randomList) != 0:
    randomItem = random.randint(0, len(randomList)-1)
    if random.randint(0, 1):
        if len(firstGroup) < numberOfCandidatesAtFirstGroup:
            firstGroup.append(randomList[randomItem])
            randomList.remove(randomList[randomItem])
    else:
        if len(secondGroup) < numberOfCandidatesAtSecondGroup:
            secondGroup.append(randomList[randomItem])
            randomList.remove(randomList[randomItem])

# Delete later
firstGroup = ['011000', '111000']
secondGroup = ['010010', '001011']

print("\nFirst group:", firstGroup)
print("Second group:", secondGroup)

parentsList = findMaxFromPopulations(firstGroup, secondGroup)

print("\nCandidates to parents:", parentsList)
parentsList = crossingOver(parentsList)
print("After crossing over:", parentsList)
