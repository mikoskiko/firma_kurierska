import numpy as np
import matplotlib.pyplot as plt
import random
import csv
import sys

print("Proszę podać ilość paczek do rozwiezienia: ")

city_size = 100
number_of_points = int(input())

# tworzenie macierzy punktów 0,0
point = []
rows = number_of_points
cols = 2

for i in range(rows):
    row = []
    for j in range(cols):
        row.append(0)
    point.append(row)
    

# losowanie punktów bez powtórzeń
middle = int(city_size/2)
point[0] = [int(middle),int(middle)]

i = 1
while i<number_of_points:
    x = 0
    a = [random.randint(0, city_size), random.randint(0, city_size)]
    for j in range(i):
        if point[j] == a:
            x = x+1
    if x == 0:
        point[i] = a
        i = i+1

x = []
for row in point:
    x.append(row[0])

y = []
for row in point:
    y.append(row[1])

# obliczanie odległości między punktami
distance = []
rows = number_of_points
cols = number_of_points
for i in range(rows):
    row = []
    for j in range(cols):
        row.append(0)
    distance.append(row)

for i in range (0, number_of_points):
    for j in range (i, number_of_points):
         distance[i][j] = distance[j][i] = ((x[i]-x[j])**2+(y[i]-y[j])**2)**0.5

with open('distance.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for row in distance:
        writer.writerow(row)

plt.plot(x,y,'ro')
plt.title("Wylosowane rozmieszczenie paczek.")
plt.show()

#ants
maxWorkTime = 500
candidateListSize = int(25 * number_of_points / 100)
#weights for propability
a = 2 
b = 5
c = 9 
#pheromones 
pheromones = np.ones((number_of_points, number_of_points))
minPheromonesValue = 0.01
maxPheromonesValue = 5
pheromonePersistance = 0.5
pheromoneEvaporConst = 80
#car amount optimization
vehicleCount = 10
minWorkTimeFraction = 7/9
iterationsToStuck = 5000
stuckCooldown = 0
stuckCooldownValue = 250
foundSolution = np.full(vehicleCount*2, False)
#iteration counters and algorithm end rules 
iterationCount = 0
maxIterations = 50000
withoutChange = 0
maxWithoutChange = 1000
#best solution
bestSolution = np.zeros((vehicleCount, number_of_points),dtype=int)
bestSolutionLength = np.full(vehicleCount,sys.maxsize)
bestSolutionSumLength = sys.maxsize

while(iterationCount <= maxIterations and withoutChange <= maxWithoutChange):
    routes = np.zeros((vehicleCount, number_of_points),dtype=int)
    routeCount = np.zeros(vehicleCount, dtype=int)
    routeLength = np.zeros(vehicleCount)
    isVisited = np.full(number_of_points,False)
    isVisited[0] = True
    allIsVisited = False
    currentIterationIter = 0
    while(not allIsVisited):
        if(currentIterationIter > iterationsToStuck and not foundSolution[vehicleCount]):
            stuckCooldown = stuckCooldownValue
            vehicleCount += 1
            break
        else:
            currentIterationIter += 1

        for i in range(vehicleCount):
            if(all(isVisited)):
                allIsVisited = True
                break

            startPoint = routes[i][routeCount[i]]
            candidateList = np.argpartition(distance[startPoint], candidateListSize)[:candidateListSize]
            j=0
            for candidate in candidateList:
                if (isVisited[candidate] == True):
                    candidateList = np.delete(candidateList, j)
                else: 
                    j+=1
            if(candidateList.size == 0):
                propabilty = np.zeros(number_of_points)
                for candidate in range(number_of_points):
                    if(isVisited[candidate] == True):
                        propabilty[candidate] = 0
                    else: 
                        propabilty[candidate] = pheromones[startPoint][candidate]**a * 1 / distance[startPoint][candidate]**b * (distance[startPoint][0]+distance[0][candidate]-distance[startPoint][candidate])**c
                nextPoint = np.argmax(propabilty)
            else:
                propabilty = np.zeros(candidateList.size)
                for j, candidate in enumerate(candidateList):
                    if(startPoint == 0 or distance[startPoint][0]+distance[0][candidate]-distance[startPoint][candidate] == 0):
                        propabilty[j] = pheromones[startPoint][candidate]**a * (1 / distance[startPoint][candidate])**b
                    else:
                        propabilty[j] = pheromones[startPoint][candidate]**a * (1 / distance[startPoint][candidate])**b * (distance[startPoint][0]+distance[0][candidate]-distance[startPoint][candidate])**c 
                nextPoint = random.choices(candidateList, propabilty, k=1)
                nextPoint = nextPoint[0]
            isVisited[nextPoint] = True
            routeCount[i]+=1
            routeLength[i]+=distance[startPoint][nextPoint] 
            routes[i][routeCount[i]] = nextPoint

            if((routeLength[i] + distance[routes[i][routeCount[i]]][0]) > maxWorkTime):
                for j in range(routeCount[i]+1):
                    isVisited[routes[i][j]] = False
                    routes[i][j] = 0
                routeLength[i] = 0
                routeCount[i] = 0
                isVisited[routes[i][0]] = True

    if(stuckCooldown == stuckCooldownValue):
        stuckCooldown-=1 
        continue
    else:
        stuckCooldown-=1

    foundSolution[vehicleCount]=True

    sumRouteLength = 0
    for i in range(vehicleCount):
        routeLength[i] += distance[routes[i][routeCount[i]]][0]
        sumRouteLength += routeLength[i]

    #evaporation of pheromones and pheromone depositon
    if(sumRouteLength < bestSolutionSumLength):
        if(any(routeLen < maxWorkTime * minWorkTimeFraction for routeLen in routeLength) and vehicleCount>1 and stuckCooldown < 1):
            vehicleCount -= 1
        withoutChange = 0
        bestSolutionCount = routeCount
        bestSolution = routes
        bestSolutionLength = routeLength
        bestSolutionSumLength = sumRouteLength
        for i in range(number_of_points):
            for j in range(number_of_points):
                pheromones[i][j] = max(minPheromonesValue, pheromones[i][j] * min(1, (pheromonePersistance + pheromoneEvaporConst/np.average(routeLength)) ))
        for j, solution in enumerate(routes):
            for i in range(1, routeCount[j]):
                pheromones[solution[i-1]][solution[i]] = pheromones[solution[i]][solution[i-1]] = min(maxPheromonesValue, pheromones[solution[i]][solution[i-1]] + maxWorkTime/routeLength[j])
    else:
        withoutChange += 1

    print("Iteracja numer: " + str(iterationCount))
    iterationCount += 1
print("Rozwiazanie")
print("Ilosc punktow na pojazd")
print(bestSolutionCount)
print("Dlugosc sciezek pojazdu")
print(bestSolutionLength)
print("Punkty odwiedzone przez pojazd")
print(bestSolution)

lineColors=['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'white', '#00FF00', '#800000', '#A52A2A', '#E5CCFF', "003300"]
plt.plot(x,y,'ro')
for j, vehicleRoute in enumerate(bestSolution):
    firstZero = True
    for i, route in enumerate(vehicleRoute):
        plt.plot([point[vehicleRoute[i]][0], point[vehicleRoute[i-1]][0] ],[point[vehicleRoute[i]][1] ,point[vehicleRoute[i-1]][1]], color=lineColors[j] ,linestyle='--')
        if(route == 0):
            if(firstZero):
                firstZero=False
                continue
            else:
                break
plt.show()