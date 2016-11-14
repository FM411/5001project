# -*- coding:utf-8 -*-
#
import xgboost
import csv
import numpy
from sklearn import neural_network
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
import math

inputFile = file("../../other_data/2802/1_全部都是零一.csv", "rb")
fileReader = csv.reader(inputFile)

trainingDataXList = []
trainingDataYList = []
count = 0
for line in fileReader:
	if count != 0:
		temp = []
		for item in line:
			temp.append(float(item))

		trainingDataXList.append(temp[:-1])
		trainingDataYList.append(math.log(10, temp[-1] + 0.01))
	count += 1


testList = []
for item in trainingDataXList:
	testList.append(len(item))

#print testList
#print len(set(testList))
print len(trainingDataXList)
print len(trainingDataYList)


X = numpy.array(trainingDataXList)
Y = numpy.array(trainingDataYList)

MLPRegressor = neural_network.MLPRegressor()

scoreList = []
kfold = KFold(n_splits = 2)
for trainIndex, testIndex in kfold.split(trainingDataXList):
	X_train, X_test = X[trainIndex], X[testIndex]
	y_train, y_test = Y[trainIndex], Y[testIndex]

	MLPRegressor.fit(X_train, y_train)
	score = MLPRegressor.score(X_test, y_test)

	scoreList.append(score)

print scoreList

#metric = cross_val_score(MLPRegressor, trainingDataXList, trainingDataYList, cv = 2)
#print metric