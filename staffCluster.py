# -*- coding:utf-8 -*-

import csv
import math
from sklearn.cluster import KMeans

inputFile = file("./other_data/sta_result3.csv", "rb")
reader = csv.reader(inputFile)

outputFile = file("./other_data/cluster3.csv", "w")
writer = csv.writer(outputFile)

staffList = []
for line in reader:
	staff = []
	name = line[0]
	movieNum = int(line[2])

	boxList = line[1].split(";")[:-1]
	average = 0
	for boxStr in boxList:
		average += float(boxStr)

	average = average / int(line[2])

	print "average: " + str(average)

	#temp = math.pow(math.log(10, average + 0.01), 2) + math.pow(movieNum, 2)
	#length = math.sqrt(temp)

	#print "length: " + str(length)


	staff.append(name)
	staff.append(math.log(10, average + 0.01))
	staff.append(movieNum)

	#staff.append(math.log(10, average + 0.01) / length)
	#staff.append(float(movieNum) / length)

	staffList.append(staff)

kmeansList = []
for item in staffList:
	kmeansList.append(item[1:])

print len(kmeansList)
num_clusters = 10
clf = KMeans(n_clusters=num_clusters)
clf.fit(kmeansList)

print list(clf.labels_)
print clf.cluster_centers_
print clf.inertia_

if len(list(clf.labels_)) != len(staffList):
	print "fuck you"

for i in xrange(len(staffList)):
	writer.writerow([staffList[i][0], staffList[i][1], staffList[i][2], clf.labels_[i]])