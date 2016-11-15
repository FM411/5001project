# -*- coding:utf-8 -*-
#
import xgboost
from sklearn import svm
from sklearn import neural_network
from sklearn import linear_model
import csv
import numpy
import math
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold

#use this for xgboost, because it can not use the sklearn style function cross_val_score()
#the score function can only use r2
def kfold(X, Y, model, fold_num):
	scoreList = []
	kfold = KFold(n_splits = fold_num)
	for trainIndex, testIndex in kfold.split(X):
		X_train, X_test = X[trainIndex], X[testIndex]
		y_train, y_test = Y[trainIndex], Y[testIndex]

		model.fit(X_train, y_train)
		score = model.score(X_test, y_test)

		scoreList.append(score)

	print "xgboost"
	print scoreList
	print numpy.average(numpy.array(scoreList))
	print

inputFile = file("./数据2/A7B1C1/2_A7B1C1_50.csv", "rb")
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
		trainingDataYList.append(temp[-1])
		#trainingDataYList.append(math.log(10, temp[-1] + 0.01))

	count += 1

#for debug ---------------
#
testList = []
for item in trainingDataXList:
	testList.append(len(item))

#print testList
#print len(set(testList))
#print trainingDataXList
#print trainingDataYList
#print len(trainingDataXList)
#print len(trainingDataYList)

#-------------------------

X = numpy.array(trainingDataXList)
Y = numpy.array(trainingDataYList)

fold_num = 5

xgb = xgboost.XGBRegressor()
kfold(X, Y, xgb, 10)

#'linear', 'poly', 'rbf', 'sigmoid', 'precomputed'
modelList = []
modelList.append(["lrRegression", linear_model.LinearRegression(normalize = True)])
modelList.append(["svr", svm.SVR(kernel='rbf')])
modelList.append(["MLPRegressor", neural_network.MLPRegressor()])

#score method: neg_mean_absolute_error, neg_mean_squared_error, neg_median_absolute_error, r2
for line in modelList:
	metric = cross_val_score(line[1], trainingDataXList, trainingDataYList, cv = fold_num, scoring = 'neg_mean_squared_error')

	print line[0]
	print metric
	print numpy.average(metric)
	print