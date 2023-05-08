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
routes = np.zeros((vehicleCount, number_of_points))
routeLength = np.zeros(vehicleCount)
pheromones = np.ones((number_of_points, number_of_points))
while(not any(isVisited) or iterationCount >= maxIterations):
    for i in range(vehicleCount):
        if(capacity[i] > maxCapacity or routeLength[i] + distance[routes[i]][0] > maxWorkTime):
            for j in range(routeLength[i]):
                isVisited[routes[i][j]] = False
                routes[i][j] = 0
            routeLength[i] = 0
        if(routeLength[i]==0):
            startPoint = random.randint(1,number_of_points)
            isVisited[startPoint] = True
            routeLength[i] = 1
            routes[i][0] = startPoint
        else:
            startPoint = routes[i][routeLength[i]-1]

        candidateList = np.argpartition(distance[startPoint], candidateListSize+1)[1:candidateListSize+1]
        for j, candidate in enumerate(candidateList):
            if (isVisited[candidate] == True):
                candidateList.delete(j)
        if(candidateList.size == 0):
            propabilty = np.zeros(number_of_points)
            for j in range(number_of_points):
                if(isVisited[j] == True):
                    propabilty[j] = sys.maxint
                else: 
                    propabilty[j] = pheromones[startPoint][candidate] * 1 / distance[startPoint][candidate] * (distance[startPoint][0]+distance[0][candidate]-distance[startPoint][candidate])
            nextPoint = propabilty.argmax(propabilty)
        else:
            propabilty = np.zeros(candidateList.size)
            for j, candidate in enumerate(candidateList):
                propabilty[j] = pheromones[startPoint][candidate] * 1 / distance[startPoint][candidate] * (distance[startPoint][0]+distance[0][candidate]-distance[startPoint][candidate]) 
            nextPoint = random.choices(candidateList, propabilty, k=1)
        routeLength[i]+=1
        routes[i][routeLength] = nextPoint


iterationCount += 1