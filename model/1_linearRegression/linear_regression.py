# -*- coding:utf-8 -*-
#
import xgboost
import csv
import numpy
from sklearn import linear_model
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

#for debug ---------------
#
testList = []
for item in trainingDataXList:
	testList.append(len(item))

#print testList
#print len(set(testList))
print len(trainingDataXList)
print len(trainingDataYList)

#-------------------------

X = numpy.array(trainingDataXList)
Y = numpy.array(trainingDataYList)
#lrModel = sklearn.LinearRegression()
lrModel = linear_model.LinearRegression(normalize = True)

scoreList = []
kfold = KFold(n_splits = 5)
for trainIndex, testIndex in kfold.split(trainingDataXList):
	X_train, X_test = X[trainIndex], X[testIndex]
	y_train, y_test = Y[trainIndex], Y[testIndex]

	lrModel.fit(X_train, y_train)
	score = lrModel.score(X_test, y_test)

	scoreList.append(score)
	print score
print scoreList

#metric = cross_val_score(lrModel, trainingDataXList, trainingDataYList, cv = 5)
#print metric