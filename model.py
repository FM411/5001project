# -*- coding:utf-8 -*-
#
import xgboost
import numpy as np
from sklearn import svm
from sklearn import neural_network
from sklearn import linear_model
import csv
import numpy
import math
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold

from sklearn.preprocessing import normalize
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LassoCV
from sklearn.linear_model import Ridge
from sklearn.feature_selection import RFE
from sklearn.grid_search import GridSearchCV



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

inputFile = file(u"./数据1/A2B1C1用演员搜索量的平均/1_A2B1C1.csv", "rb")
# inputFile = file(u'C:/Users/User/Desktop/simple_mf.csv','rb')
fileReader = csv.reader(inputFile)

trainingDataXList = []
trainingDataYList = []
count = 0
for line in fileReader:
	if count != 0:
		temp = []
		for item in line[12:]:
			# if item == '':
			# 	temp.append(float(0))
			# 	continue
            #
			temp.append(float(item))


		trainingDataXList.append(temp[:-1])
		trainingDataYList.append(temp[-1])
		#trainingDataYList.append(math.log(10, temp[-1] + 0.01))

	count += 1


# #feature selection
# X = np.array(trainingDataXList)
# y = np.array(trainingDataYList)
#
# print X.shape
#
# model = Ridge()
# alphas = np.array([1,0.1,0.01,0.001,0.0001,0])
# grid = GridSearchCV(estimator=model,param_grid=dict(alpha = alphas))
# grid.fit(X,y)
# print grid
# print grid.best_score_
# print grid.best_estimator_


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

# X = normalize(X)

fold_num = 5

xgb = xgboost.XGBRegressor()
kfold(X, Y, xgb, 10)

#'linear', 'poly', 'rbf', 'sigmoid', 'precomputed'
modelList = []
modelList.append(["lrRegression", linear_model.LinearRegression(normalize = True)])
modelList.append(["svr", svm.SVR(kernel='rbf')])
modelList.append(["MLPRegressor", neural_network.MLPRegressor()])

# testfile = file(u'../电影票房数据文件/')


#score method: neg_mean_absolute_error, neg_mean_squared_error, neg_median_absolute_error, r2
for line in modelList:
	metric = cross_val_score(line[1], trainingDataXList, trainingDataYList, cv = fold_num, scoring = 'neg_mean_squared_error')

	print line[0]
	print metric
	print numpy.average(metric)
	print