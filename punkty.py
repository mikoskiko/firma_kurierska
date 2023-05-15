import numpy as np
import matplotlib.pyplot as plt
import random
import csv
import sys

#np.set_printoptions(threshold=sys.maxsize)

city_size = 1000
number_of_points = 100

# tworzenie macierzy punktów 0,0
point = []
rows = number_of_points
cols = 2

for i in range(rows):
    row = []
    for j in range(cols):
        row.append(0)
    point.append(row)
    

point[0] = [int(city_size/2),int(city_size/2)]
    
for i in range(1, number_of_points):
    point[i] = [random.randint(0, city_size),random.randint(0,city_size)]

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
maxWorkTime = 6000
maxCapacity = 8
maxIterations = 50000
iterationCount = 0

candidateListSize = int(25 * number_of_points / 100)
pheromones = np.full((number_of_points, number_of_points), 2*vehicleCount/maxWorkTime)
bestSolution = np.zeros((vehicleCount, number_of_points),dtype=int)
bestSolutionLength = np.full(vehicleCount,sys.maxsize)
bestSolutionSumLength = sys.maxsize

while(iterationCount <= maxIterations):
    capacity = np.zeros(vehicleCount)
    routes = np.zeros((vehicleCount, number_of_points),dtype=int)
    routeCount = np.zeros(vehicleCount, dtype=int)
    routeLength = np.zeros(vehicleCount)
    isVisited = np.full(number_of_points,False)
    isVisited[0] = True
    allIsVisited=False
    while(not allIsVisited):
        for i in range(vehicleCount):
            if(all(isVisited)):
                allIsVisited = True
                break
            if(routeCount[i]==0):
                while(True):
                    startPoint = random.randint(1,number_of_points-1)
                    if(isVisited[startPoint]==False):
                        break
                isVisited[startPoint] = True
                routeLength[i] = distance[0][startPoint]
                routeCount[i] = 1
                routes[i][routeCount[i]] = startPoint

            startPoint = routes[i][routeCount[i]]
            candidateList = np.argpartition(distance[startPoint][1:number_of_points-1], candidateListSize)[:candidateListSize]
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
                        propabilty[candidate] = pheromones[startPoint][candidate] * 1 / distance[startPoint][candidate] * (distance[startPoint][0]+distance[0][candidate]-distance[startPoint][candidate])
                nextPoint = np.argmax(propabilty)
            else:
                propabilty = np.zeros(candidateList.size)
                for j, candidate in enumerate(candidateList):
                    if(startPoint == 0 ):
                        propabilty[j] = pheromones[startPoint][candidate] * (1 / distance[startPoint][candidate])
                    else:
                        propabilty[j] = pheromones[startPoint][candidate] * (1 / distance[startPoint][candidate]) * (distance[startPoint][0]+distance[0][candidate]-distance[startPoint][candidate]) 
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

    sumRouteLength = 0
    for i in range(vehicleCount):
        routeLength[i] += distance[routes[i][routeCount[i]]][0]
        sumRouteLength += routeLength[i]

    #evaporation of pheromones
    for i in range(number_of_points):
        for j in range(number_of_points):
            pheromones[i][j] = max(0.01, pheromones[i][j] - (vehicleCount/maxWorkTime/100 + 5/np.average(routeLength)))
    #pheromone depositon
    if(sumRouteLength < bestSolutionSumLength):
        bestSolutionCount = routeCount
        bestSolution = routes
        bestSolutionLength = routeLength
        bestSolutionSumLength = sumRouteLength

    for j, solution in enumerate(bestSolution):
        for i in range(1, bestSolutionCount[j]):
            pheromones[solution[i-1]][solution[i]] = pheromones[solution[i]][solution[i-1]] = pheromones[solution[i]][solution[i-1]] + 100/distance[solution[i]][solution[i-1]]
    print(pheromones)
    print("--------------")
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