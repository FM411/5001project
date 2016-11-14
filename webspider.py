# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import urllib2,urllib,sys
import re
import csv
from time import sleep

boxFile = file('./电影票房数据文件/box.csv', 'rb')
metadataFile = file('./电影票房数据文件/metadata.csv', 'rb')
relationFile = file('./电影票房数据文件/relation.csv', 'rb')

boxReader = csv.reader(boxFile)
metadataReader = csv.reader(metadataFile)
relationReader = csv.reader(relationFile)

#----------------------------------------------------------------------


movieValueFile = file('./搜索量/movieValue.csv', 'rb')
movieValueReader = csv.reader(movieValueFile)
movieNameAlreadyHasList = []
for line in movieValueReader:
	movieNameAlreadyHasList.append(line[0])
movieValueFile.close()


relationValueFile = file('./搜索量/relationValue.csv', 'rb')
relationValueReader = csv.reader(relationValueFile)
relationAlreadyHasList = []
for line in relationValueReader:
	relationAlreadyHasList.append(line[0])
relationValueFile.close()

#----------------------------------------------------------------------

movieValueFile = file('./搜索量/movieValue.csv', 'a')
relationValueFile = file('./搜索量/relationValue.csv', 'a')

movieValueWriter = csv.writer(movieValueFile)
relationValueWriter = csv.writer(relationValueFile)

movieNameList = []
relationList = []

count = 0
for line in boxReader:
	if count >= 1:
		movieNameList.append(line[0])

	count += 1

count = 0
for line in metadataReader:
	if count >= 1:
		movieNameList.append(line[0])
	count += 1

count = 0
for line in relationReader:
	if count >= 1:
		relationList.append(line[1])
	count += 1

movieNameList = list(set(movieNameList))
relationList = list(set(relationList))

movieNameValueList = []
relationValueList = []

"""
for movieName in movieNameList:
	movieValueWriter.writerow([movieName])
"""

for movieName in movieNameList:
	print "movieName: " + movieName
	if movieName != "" and movieName not in movieNameAlreadyHasList:
		url = "http://www.baidu.com/s"
		search = [('wd', movieName)]
		getString = url + "?" + urllib.urlencode(search)

		request = urllib2.Request(getString)
		fd = urllib2.urlopen(request)
		soup = BeautifulSoup(fd.read())
		#print soup

		searchList = soup.find(class_= "nums")
		pattern = re.findall(r'搜索工具百度为您找到相关结果约(.*)个', searchList.getText().encode("utf-8"))
		print
		print searchList.getText()
		#print pattern[0]

		numberStr = pattern[0].replace(",", "")
		print numberStr

		movieValueWriter.writerow([movieName, numberStr])
		sleep(0.05)



for relation in relationList:
	print len(relationList)
	print "relationName: " + relation
	if relation != "" and relation not in relationAlreadyHasList:
		url = "http://www.baidu.com/s"
		search = [('wd', relation)]
		getString = url + "?" + urllib.urlencode(search)

		request = urllib2.Request(getString)
		fd = urllib2.urlopen(request)
		soup = BeautifulSoup(fd.read())
		#print soup

		searchList = soup.find(class_= "nums")
		pattern = re.findall(r'搜索工具百度为您找到相关结果约(.*)个', searchList.getText().encode("utf-8"))
		print
		print searchList.getText()
		#print pattern[0]

		numberStr = pattern[0].replace(",", "")
		print numberStr

		relationValueWriter.writerow([relation, numberStr])
		sleep(0.05)

boxFile.close()
metadataFile.close()
relationFile.close()
movieValueFile.close()
relationValueFile.close()