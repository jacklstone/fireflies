#!/usr/local/bin/python3
import random
import cv2
from math import sin, pi, ceil
import numpy as np
def createLocations(x, y, z, threshold, r):
  return np.array([[int(random.uniform(0, x)), int(random.uniform(0, y)), 0, random.uniform((1-periodRange/2)*threshold,(1+periodRange/2)*threshold)] for t in range(z)])

def inverseDistance(t, j, loc, disDict):
	if t > j: t,j = j,t
	if (t,j) in disDict: return disDict[(t,j)]
	dis = ((loc[j][0] - loc[t][0]) ** 2 + (loc[j][1] - loc[t][1]) ** 2) ** 0.5
	invDis = min(1,1.0 / dis)
	disDict[(t,j)] = invDis
	return invDis


def drawImage(y, x, loc, r):
	img=np.zeros((x,y,3)).astype(np.uint8)
	for c in loc:
	  value = (1 - c[2] / c[3])
	  for i in range(r-1, -1, -1):
			temp = value - .04*i
			if temp > 0:
				color = (255*2*(temp-0.5), 255, 255) if temp > 0.5 else (0, 255 * 2 * temp, 255 * 2 * temp)
				cv2.circle(img, (int(c[0]), int(c[1])), i+1, color, -1)
	cv2.imshow("Fireflies",img)
	k = cv2.waitKey(1)
	if (k == 27 or k == ord('q')):
		return 1
	return 0

def run(x, y, z, r, b, alpha, threshold, stillness, maxMove, moveDuration, epsilon, convergenceFactor):
	maxDist = x**2 + y**2

	loc = createLocations(x, y, z, threshold, r)
	disDict = {}

	movementPhase = [0 for t in loc]
	target = [(t[0],t[1]) for t in loc]

	tick = 0
	flag = 0

	while(True):
		if(tick % ceil(stillness) == ceil(stillness) - 1):
			for s in range(int(1/stillness)):
				t = random.randrange(0,z)
				if(movementPhase[t] == 0):
					movementPhase[t] = 1
					deltaX = random.randint(-maxMove,maxMove)
					deltaY = random.randint(-maxMove,maxMove)
					targetX = loc[t][0] + deltaX
					targetY = loc[t][1] + deltaY
					if (targetX != targetX % x):
						targetX -= 2 * deltaX
					if (targetY != targetY % y):
						targetY -= 2 * deltaY
					target[t] = targetX, targetY
		periods = [t[3] for t in loc]
		maxPeriod = max(periods)
		minPeriod = min(periods)
		if flag == 0:
			if minPeriod/maxPeriod > convergenceFactor: 
				print("Periods equal")
				flag = 1

		for t in range(len(loc)):
			if (movementPhase[t] != 0):
				loc[t][0] = (loc[t][0] + (movementPhase[t] * (target[t][0] - loc[t][0])) //moveDuration) % x
				loc[t][1] = (loc[t][1] + (movementPhase[t] * (target[t][1] - loc[t][1])) //moveDuration) % y
				movementPhase[t] = (movementPhase[t] + 1) % moveDuration
			loc[t][2]+=(threshold-loc[t][2]) * alpha
			if loc[t][2] > loc[t][3]:
				for j in range(len(loc)):
					if t != j:
						invDis = inverseDistance(t,j,loc,disDict)
						if flag:
							loc[j][2] += (b * invDis * (loc[j][2]/loc[j][3]))
						else:
							loc[j][3] += (b * invDis * sin(loc[t][3] - loc[j][3]))
				loc[t][2] = 0
		tick+=1
		if (drawImage(x, y, loc, r)):
			break

x = 1280
y = 700
z = 100
r = 5

b = 100 / z
alpha = pi/20
threshold = 2*pi
periodRange = .4

stillness = .01
maxMove = 100
moveDuration = 10

epsilon = 10
convergenceFactor = .9995

run(x, y, z, r, b, alpha, threshold, stillness, maxMove, moveDuration, epsilon, convergenceFactor)
