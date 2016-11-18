# -*- coding:utf-8 -*-

import csv
import datetime
import collections
import urllib2,urllib,re
from time import sleep

from bs4 import BeautifulSoup

inputfile = file(u'./数据1/1_middle.csv','rb')
reader = csv.reader(inputfile)

source_data = []
month_box = collections.defaultdict(float)
theme_box = collections.defaultdict(float)
theme_count = collections.defaultdict(int)

row1 = []
row2 = []
sum_up = 0.0
for line in reader:
    record = []
    month_record = []
    release = line[2]
    if '/' not in release:
        continue
    release = datetime.datetime.strptime(release,"%Y/%m/%d").date()
    box_total = float(line[8])
    name = line[0]
    theme = line[1].split('/')

    record.append(name)
    record.append(theme)

    month_record.append(name)
    month_record.append(release.month)

    for i in theme:
        theme_box[i] += box_total
        theme_count[i] += 1
    month_box[release.month] += box_total
    sum_up += box_total

    row1.append(record)
    row2.append(month_record)
    # record.append(release)
    # record.append(box_total)
    # # record.append(name)
    # source_data.append(record)



outputfile = file(u'./数据1/type_middle.csv','wb')
writer = csv.writer(outputfile)
writer.writerow(['Moviename','Type','weight'])

outputfile2 = file(u'./数据1/month_middle.csv','wb')
writer2 = csv.writer(outputfile2)
writer2.writerow(['Moviename','month','weight'])

for x in row1:
    sm = 0
    for type in x[1]:
        sm += theme_box[type]
    x.append(sm/sum_up)
    x[1] = '/'.join(x[1])

    writer.writerow(x)

for mm in row2:
    mm.append(month_box[mm[1]]/sum_up)
    writer2.writerow(mm)

for type in theme_box.keys():
    ln = [type,theme_box[type]]
    aver = theme_box[type]/sum_up
    ln.append(aver)
    writer.writerow(ln)

for month in month_box.keys():
    ln = [month,month_box[month]]
    aver = month_box[month]/sum_up
    ln.append(aver)
    writer2.writerow(ln)

print month_box
print theme_box
print theme_count
print sum_up

"""
TypeSearch = file(u'./搜索量/typeValue.csv','wb')
Typewriter = csv.writer(TypeSearch)

for type in theme_box.keys():
    print "TypeName: " + type
    if type != "":
		url = "http://www.baidu.com/s"
		search = [('wd', type+' 电影')]
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

		Typewriter.writerow([type, numberStr])
		sleep(0.05)




#
# inputfile.close()
# outputfile.close()

"""