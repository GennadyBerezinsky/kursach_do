import random

def startMenu():
    answerIsCorrect = False
    while answerIsCorrect != True:
        print("Program has been developed by Ilienko Roman and Berezinsky Genadiy IS-63")
        print("How do you want to fill animal's matrix?")
        try:
            answer = int(input("1. By your own\n2. Random generate\n3. From file\n4. From work example\nYour answer is: "))
            if answer <= 4:
                answerIsCorrect = True
        except Exception:
            print("Incorrect input, try again..")

    if answer == 4:
        startMatrix = [
            [1, 1, 1, 0, 1, 0],
            [1, 1, 1, 0, 1, 0],
            [1, 1, 1, 0, 1, 1],
            [0, 0, 0, 1, 1, 0],
            [1, 1, 1, 1, 1, 1],
            [0, 0, 1, 0, 1, 1]
        ]
    
    return startMatrix

startMatrix = startMenu()

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
    for count, element in enumerate(item, start = 0):
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

def crossingOver(parentsList):
    firstBlockSize = random.randint(1, int(len(parentsList[0])/2))
    secondBlockSize = len(parentsList[0]) - firstBlockSize

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

matrixLen = len(startMatrix)

populationList = []

for i in range(16):
    randomPopulation = getRandomPopulation(matrixLen)
    if populationList.count(randomPopulation) == 0:
        populationList.append(randomPopulation)

bestSolution = ['', 0]

print("Generated population:")
whatToDelete = []
for count, populationItem in enumerate(populationList, start = 0):
    printPopulations(count + 1, startMatrix, populationItem)
    if checkIfSatisfy(startMatrix, populationItem)[0] == False:
        whatToDelete.append(populationItem)
    
for element in whatToDelete:
    populationList.remove(element)


print("\nCleaned population:")
for count, populationItem in enumerate(populationList, start = 0):
    printPopulations(count + 1, startMatrix, populationItem)
    if countAnimals(populationItem) > bestSolution[1]:
        bestSolution[0] = populationItem
        bestSolution[1] = countAnimals(populationItem)

print("\nNow the best is", bestSolution[0], "with", bestSolution[1], "animals")

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

    print("\nFirst group:", firstGroup)
    print("Second group:", secondGroup)

    parentsList = findMaxFromPopulations(firstGroup, secondGroup)

    print("\nCandidates to parents:", parentsList)
    descendantList = crossingOver(parentsList)
    print("After crossing over:", descendantList)

    for count, descendant in enumerate(descendantList, start = 0):
        if random.randint(0, 10) == 1:
            randomAnimal = random.randint(0, len(descendant)-1)
            if descendant[randomAnimal] == '1':
                descendant = changeChar(descendant, randomAnimal, "0")
            else:
                descendant = changeChar(descendant, randomAnimal, "1")
        descendantList[count] = descendant

    print("After mutation with 0.1 probability:")

    for count, descendant in enumerate(descendantList, start = 0):
        printPopulations(count, startMatrix, descendant)

    for count, descendant in enumerate(descendantList, start = 0):
        isCorrect, agressiveList = checkIfSatisfy(startMatrix, descendantList[count])
        if isCorrect == False:
            print("\nReanimation...", descendantList[count])
            while isCorrect != True:
                mostAgressiveAnimal = [0, 0]
                for animal in agressiveList:
                    if animal[1] > mostAgressiveAnimal[1]:
                        mostAgressiveAnimal[0] = animal[0]
                        mostAgressiveAnimal[1] = animal[1]
                print("The most agressive animal in", descendant, "is", mostAgressiveAnimal[0], "... Changing")
                descendantList[count] = changeChar(descendantList[count], mostAgressiveAnimal[0], "0")
                isCorrect, agressiveList = checkIfSatisfy(startMatrix, descendantList[count])
                print("Now it is", descendantList[count], "\n")

    print("After reanimation:")

    for count, descendant in enumerate(descendantList, start = 0):
        printPopulations(count, startMatrix, descendant)
        populationList.append(descendant)

    print ("\nAdding new members to population list...")

    for count, item in enumerate(populationList, start = 0):
        printPopulations(count, startMatrix, item)

    print ("\nRemoving 2 worst...")
    populationList = find2Worst(populationList)
    for count, populationItem in enumerate(populationList, start = 0):
        printPopulations(count + 1, startMatrix, populationItem)
        if countAnimals(populationItem) > bestSolution[1]:
            bestSolution[0] = populationItem
            bestSolution[1] = countAnimals(populationItem)

    print("\nOn step", globalCount + 1,"the best is", bestSolution[0], "with", bestSolution[1], "animals")
