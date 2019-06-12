import random
import time
import sys
import json
start_time = time.time()

def returnAnimalsList(animals):
    animalsList = []
    for number, animal in enumerate(animals):
        if animal == '1':
            animalsList.append(number)
    return animalsList

def changeChar(s, p, r):
        return s[:p]+r+s[p+1:]

def getRandomPopulation(stringLength):
    letters = "01"
    return ''.join(random.choice(letters) for i in range(stringLength))

def checkAnimals(matrix, animalOneNumber, animalTwoNumber):
    return matrix[animalOneNumber][animalTwoNumber] == 1

def checkIfSatisfy(matrix, item):
    hasConflict = True
    animalNumbers = []
    for count, element in enumerate(item):
        if (element == '1'):
            animalNumbers.append([count, 0])
    for i in range(len(animalNumbers)):
        for j in range(len(animalNumbers)):
            if checkAnimals(matrix, animalNumbers[i][0], animalNumbers[j][0]) == False:
                animalNumbers[i][1] += 1
                hasConflict = False
    
    return hasConflict, animalNumbers

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
    + " " + str(checkIfSatisfy(startMatrix, populationItem)[0]))

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

def crossingOver(globalCout, parentsList):
    firstBlockSize = random.randint(1, int(len(parentsList[0])/2))
    secondBlockSize = len(parentsList[0]) - firstBlockSize
    if len(parentsList[0]) % 2 != 0:
        secondBlockSize -= 1

    firstFirstPart = parentsList[0][:firstBlockSize]
    firstSecondPart = parentsList[0][secondBlockSize:]
    secondFirstPart = parentsList[1][:firstBlockSize]
    secondSecondPart = parentsList[1][secondBlockSize:]

    parentsList[0] = firstFirstPart + secondSecondPart
    parentsList[1] = secondFirstPart + firstSecondPart

    return parentsList

def find2Worst(populationList):
    for count in range(2):
        firstIteration = True
        worstPopulation = ''
        for population in populationList:
            if firstIteration:
                worstPopulation = population
                firstIteration = False
            else:
                if countAnimals(population) < countAnimals(worstPopulation):
                    worstPopulation = population
        populationList.remove(worstPopulation)
    return populationList

try:
    lineMatrix = sys.argv[1]
    matrixSize = int(sys.argv[2])

    startMatrix = [[0 for j in range(matrixSize)] for i in range(matrixSize)]

    for i in range(matrixSize):
        for j in range(matrixSize):
            if i == j:
                startMatrix[i][j] = 1
                continue
            if j < i:
                startMatrix[i][j] = startMatrix[j][i]
                continue
            startMatrix[i][j] = int(lineMatrix[0])
            lineMatrix = lineMatrix[1:]

    matrixLen = len(startMatrix)

    populationList = []

    whileCount = 0
    trueNumbers = 0
    while whileCount <= 16 and trueNumbers < 2:
        randomPopulation = getRandomPopulation(matrixLen)
        onlyZero = True
        for letter in randomPopulation:
            if letter != '0':
                onlyZero = False
        if onlyZero:
            continue
        if populationList.count(randomPopulation) == 0:
            populationList.append(randomPopulation)
            if checkIfSatisfy(startMatrix, randomPopulation)[0] == True:
                trueNumbers += 1

    bestSolution = ['', 0]

    #print("Generated population:")
    whatToDelete = []
    for count, populationItem in enumerate(populationList, start = 0):
        #printPopulations(count + 1, startMatrix, populationItem)
        if checkIfSatisfy(startMatrix, populationItem)[0] == False:
            whatToDelete.append(populationItem)
        
    for element in whatToDelete:
        populationList.remove(element)

    #print("\nCleaned population:")
    for count, populationItem in enumerate(populationList, start = 0):
        #printPopulations(count + 1, startMatrix, populationItem)
        if countAnimals(populationItem) > bestSolution[1]:
            bestSolution[0] = populationItem
            bestSolution[1] = countAnimals(populationItem)

    #print("\nNow the best is", bestSolution[0], "with", bestSolution[1], "animals")

    for globalCount in range(20):
        numberOfCandidatesAtFirstGroup = int(len(populationList) / 2)
        numberOfCandidatesAtSecondGroup = len(populationList) - numberOfCandidatesAtFirstGroup

        firstGroup = []
        secondGroup = []

        randomList = populationList.copy()
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

        #print("\nFirst group:", firstGroup)
        #print("Second group:", secondGroup)

        parentsList = findMaxFromPopulations(firstGroup, secondGroup)

        #print("\nCandidates to parents:", parentsList)
        descendantList = crossingOver(globalCount, parentsList)
        #print("After crossing over:", descendantList)

        for count, descendant in enumerate(descendantList, start = 0):
            if random.randint(0, 10) == 1:
                randomAnimal = random.randint(0, len(descendant)-1)
                if descendant[randomAnimal] == '1':
                    descendant = changeChar(descendant, randomAnimal, "0")
                else:
                    descendant = changeChar(descendant, randomAnimal, "1")
            descendantList[count] = descendant

        #print("After mutation with 0.1 probability:")

        #for count, descendant in enumerate(descendantList, start = 0):
            #printPopulations(count, startMatrix, descendant)

        for count, descendant in enumerate(descendantList, start = 0):
            isCorrect, agressiveList = checkIfSatisfy(startMatrix, descendantList[count])
            if isCorrect == False:
                #print("\nReanimation...", descendantList[count])
                while isCorrect != True:
                    mostAgressiveAnimal = [0, 0]
                    for animal in agressiveList:
                        if animal[1] > mostAgressiveAnimal[1]:
                            mostAgressiveAnimal[0] = animal[0]
                            mostAgressiveAnimal[1] = animal[1]
                    #print("The most agressive animal in", descendant, "is", mostAgressiveAnimal[0], "... Changing")
                    descendantList[count] = changeChar(descendantList[count], mostAgressiveAnimal[0], "0")
                    isCorrect, agressiveList = checkIfSatisfy(startMatrix, descendantList[count])
                    #print("Now it is", descendantList[count], "\n")

        #print("After reanimation:")

        for count, descendant in enumerate(descendantList, start = 0):
            #printPopulations(count, startMatrix, descendant)
            populationList.append(descendant)

        #print ("\nAdding new members to population list...")

        #for count, item in enumerate(populationList, start = 0):
            #printPopulations(count, startMatrix, item)

        #print ("\nRemoving 2 worst...")
        populationList = find2Worst(populationList)
        for count, populationItem in enumerate(populationList, start = 0):
            #printPopulations(count + 1, startMatrix, populationItem)
            if countAnimals(populationItem) > bestSolution[1]:
                bestSolution[0] = populationItem
                bestSolution[1] = countAnimals(populationItem)

        #print("\nOn step", globalCount + 1,"the best is", bestSolution[0], "with", bestSolution[1], "animals")

    #print("Start matrix: ")
    #for row in startMatrix:
        #print(row)

    answer = [(time.time() - start_time), bestSolution[1], returnAnimalsList(bestSolution[0]), startMatrix]
    print(json.dumps(answer))

except:
    print("error")