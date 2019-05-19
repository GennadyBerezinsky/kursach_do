import random
import string

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
print("\nAt first group it will be " + str(numberOfCandidatesAtFirstGroup) + " elements")
print("At Second group it will be " + str(len(populationList) - numberOfCandidatesAtFirstGroup) + " elements")
    