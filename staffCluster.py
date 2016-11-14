# -*- coding:utf-8 -*-

import csv
import math
from sklearn.cluster import KMeans

#inputFile = file("./数据2/staff/sta_result_zhizuo.csv", "rb")
#inputFile = file("./数据2/staff/sta_result_daoyan.csv", "rb")
#inputFile = file("./数据2/staff/sta_result_yanyuan.csv", "rb")
#inputFile = file("./数据2/staff/sta_result_zhizuoren.csv", "rb")
inputFile = file("./数据2/staff/sta_result_faxing.csv", "rb")
reader = csv.reader(inputFile)

#outputFile = file("./数据2/staff/staffCluster/kmeans/10-10-10-10-50/zhizhuo.csv", "w")
#outputFile = file("./数据2/staff/staffCluster/kmeans/10-10-10-10-50/daoyan.csv", "w")
#outputFile = file("./数据2/staff/staffCluster/kmeans/10-10-10-10-50/yanyuan.csv", "w")
#outputFile = file("./数据2/staff/staffCluster/kmeans/10-10-10-10-50/zhizhuoren.csv", "w")
outputFile = file("./数据2/staff/staffCluster/kmeans/10-10-10-10-50/faxing.csv", "w")
writer = csv.writer(outputFile)

staffList = []
for line in reader:
	staff = []
	name = line[0]
	movieNum = int(line[2])

	boxList = line[1].split(";")
	boxSum = 0
	for boxStr in boxList:
		boxSum += float(boxStr)

	print "boxSum: " + str(boxSum) + " log: " + str(math.log(boxSum + 0.01, 10))

	staff.append(name)
	staff.append(math.log(boxSum + 0.01, 10))
	#staff.append(movieNum)
	staffList.append(tuple(staff))

kmeansList = []
for item in staffList:
	kmeansList.append([item[1], 0])

print len(kmeansList)
num_clusters = 10
clf = KMeans(n_clusters=num_clusters)
clf.fit(kmeansList)

#print list(clf.labels_)
print clf.cluster_centers_
print clf.inertia_

classList = []
for j in xrange(num_clusters):
	classList.append([])

	for i in xrange(len(staffList)):
		if clf.labels_[i] == j:
			classList[j].append(staffList[i])

for i in xrange(len(classList)):
	classList[i] = sorted(classList[i], key=lambda x:x[1])

	for item in classList[i]:
		writer.writerow([item[0], item[1], i])

inputFile.close()
outputFile.close()