import numpy as np
import matplotlib.pyplot as plt
import random
import csv
import sys

np.set_printoptions(threshold=sys.maxsize)

city_size = 100
number_of_points = 200

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

print('point: ', point)

x = []
for row in point:
    x.append(row[0])

y = []
for row in point:
    y.append(row[1])

print("macierz x: ", x)
print("macierz y: ", y)


# obliczanie odległości między punktami
distance = []
rows = number_of_points
cols = number_of_points
for i in range(rows):
    row = []
    for j in range(cols):
        row.append(0)
    distance.append(row)

print(distance)

for i in range (0, number_of_points):
    for j in range (i, number_of_points):
         distance[i][j] = distance[j][i] = ((x[i]-x[j])**2+(y[i]-y[j])**2)**0.5
print(distance)
with open('distance.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for row in distance:
        writer.writerow(row)

plt.plot(x,y,'ro')
plt.show()

#ants
vehicleCount = 10
maxWorkTime = 500
maxCapacity = 8
maxIterations = 50000
iterationCount = 0
a = 2
b = 5
c = 9

candidateListSize = int(25 * number_of_points / 100)
pheromones = np.ones((number_of_points, number_of_points))
bestSolution = np.zeros((vehicleCount, number_of_points),dtype=int)
bestSolutionLength = np.full(vehicleCount,sys.maxsize)
bestSolutionSumLength = sys.maxsize
whithoutChange = 0
stuckCooldown = 0
foundSolution = np.full(vehicleCount*2, False)

while(iterationCount <= maxIterations):
    capacity = np.zeros(vehicleCount)
    routes = np.zeros((vehicleCount, number_of_points),dtype=int)
    routeCount = np.zeros(vehicleCount, dtype=int)
    routeLength = np.zeros(vehicleCount)
    isVisited = np.full(number_of_points,False)
    isVisited[0] = True
    allIsVisited=False
    currentIterationIter = 0
    while(not allIsVisited):
        for i in range(vehicleCount):
            if(all(isVisited)):
                allIsVisited = True
                break
            #if(routeCount[i]==0):
             #   while(True):
              #      startPoint = random.randint(1,number_of_points-1)
               #     if(isVisited[startPoint]==False):
               #         break
               #isVisited[startPoint] = True
               #routeLength[i] = distance[0][startPoint]
               #routeCount[i] = 1
               #routes[i][routeCount[i]] = startPoint

            startPoint = routes[i][routeCount[i]]
            candidateList = np.argpartition(distance[startPoint], candidateListSize)[:candidateListSize]
            j=0
            for candidate in candidateList:
                if (isVisited[candidate] == True or startPoint==candidate):
                    candidateList = np.delete(candidateList, j)
                else: 
                    j+=1
            if(candidateList.size == 0):
                propabilty = np.zeros(number_of_points)
                for candidate in range(number_of_points):
                    if(isVisited[candidate] == True):
                        propabilty[candidate] = -1
                    else: 
                        propabilty[candidate] = pheromones[startPoint][candidate]**a * 1 / distance[startPoint][candidate]**b * (distance[startPoint][0]+distance[0][candidate]-distance[startPoint][candidate])**c
                nextPoint = np.argmax(propabilty)
            else:
                propabilty = np.zeros(candidateList.size)
                for j, candidate in enumerate(candidateList):
                    if(startPoint == 0 ):
                        propabilty[j] = pheromones[startPoint][candidate]**a * (1 / distance[startPoint][candidate])**b
                    else:
                        propabilty[j] = pheromones[startPoint][candidate]**a * (1 / distance[startPoint][candidate])**b * (distance[startPoint][0]+distance[0][candidate]-distance[startPoint][candidate])**c 
                nextPoint = random.choices(candidateList, propabilty, k=1)
                nextPoint = nextPoint[0]
            isVisited[nextPoint] = True
            routeCount[i]+=1
            routeLength[i]+=distance[startPoint][nextPoint] 
            routes[i][routeCount[i]] = nextPoint

            if(capacity[i] > maxCapacity or (routeLength[i] + distance[routes[i][routeCount[i]]][0]) > maxWorkTime):
                for j in range(routeCount[i]+1):
                    isVisited[routes[i][j]] = False
                    routes[i][j] = 0
                routeLength[i] = 0
                routeCount[i] = 0
                isVisited[routes[i][0]] = True
        if(currentIterationIter > 5000 and not foundSolution[vehicleCount]):
            stuckCooldown = 250
            vehicleCount += 1
            break
        else:
            currentIterationIter += 1

    if(stuckCooldown == 250):
        stuckCooldown-=1 
        continue
    else:
        stuckCooldown-=1

    foundSolution[vehicleCount]=True

    sumRouteLength = 0
    for i in range(vehicleCount):
        routeLength[i] += distance[routes[i][routeCount[i]]][0]
        sumRouteLength += routeLength[i]

    #heurestics

    #evaporation of pheromones
    #pheromone depositon
    if(sumRouteLength < bestSolutionSumLength):
        if(any(routeLen < maxWorkTime*7/9 for routeLen in routeLength) and vehicleCount>1 and stuckCooldown < 1):
            vehicleCount -= 1
        withoutChange = 0
        bestSolutionCount = routeCount
        bestSolution = routes
        bestSolutionLength = routeLength
        bestSolutionSumLength = sumRouteLength
        for i in range(number_of_points):
            for j in range(number_of_points):
                pheromones[i][j] = max(0.01, pheromones[i][j] - (0.8 + 80/np.average(routeLength)))
        for j, solution in enumerate(routes):
            for i in range(1, routeCount[j]):
                pheromones[solution[i-1]][solution[i]] = pheromones[solution[i]][solution[i-1]] = pheromones[solution[i]][solution[i-1]] + 10/distance[solution[i]][solution[i-1]]
        #print(pheromones)
        #print("--------------")
    else:
        withoutChange += 1
        if(withoutChange==1000):
            break

    print(routeCount)
    print("--------------")
    print(routeLength)
    print("--------------")
    print(routes)
    print("----iter----------")
    iterationCount += 1
print(bestSolutionCount)
print("--------------")
print(bestSolutionLength)
print("--------------")
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

#con=np.concatenate((routes[0],routes[1],routes[2],routes[3],routes[4],routes[5],routes[6],routes[7],routes[8],routes[9]))
#sor=np.sort(con)
#print(sor)
