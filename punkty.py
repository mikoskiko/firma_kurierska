import numpy as np
import matplotlib.pyplot as plt
import random
import csv
import sys

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
maxWorkTime = 1000000
maxCapacity = 8
maxIterations = 100000
iterationCount = 0
candidateListSize = int(10 * number_of_points / 100)
isVisited = np.full(number_of_points,False)
isVisited[0] = True
capacity = np.zeros(vehicleCount)
routes = np.zeros((vehicleCount, number_of_points),dtype=int)
routeCount = np.zeros(vehicleCount, dtype=int)
routeLength = np.zeros(vehicleCount)
pheromones = np.ones((number_of_points, number_of_points))
while(not all(isVisited) and iterationCount <= maxIterations):
    for i in range(vehicleCount):
        print( routeCount[i])

        if(capacity[i] > maxCapacity or (routeLength[i] + distance[routes[i][routeCount[i]]][0]) > maxWorkTime):
            for j in range(routeLength[i]):
                isVisited[routes[i][j]] = False
                routes[i][j] = 0
            routeLength[i] = 0
            routeCount[i] = 0
        if(routeLength[i]==0):
            startPoint = random.randint(1,number_of_points-1)
            isVisited[startPoint] = True
            routeLength[i] = distance[0][startPoint]
            routes[i][routeCount[0]] = startPoint
            routeCount[i] = 1
        else:
            startPoint = routes[i][routeCount[i]-1]

        candidateList = np.argpartition(distance[startPoint], candidateListSize+1)[:candidateListSize+1]
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
                propabilty[j] = pheromones[startPoint][candidate] * 1 / distance[startPoint][candidate] * (distance[startPoint][0]+distance[0][candidate]-distance[startPoint][candidate]) 
            nextPoint = random.choices(candidateList, propabilty, k=1)
            nextPoint = nextPoint[0]
        isVisited[nextPoint] = True
        routeLength[i]+=distance[i][routeCount[i]] 
        routes[i][routeCount[i]] = nextPoint
        routeCount[i]+=1

iterationCount += 1
print(routes)