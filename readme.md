
### 合并raw data

将box，metadata，relation单个表信息汇总后，没有进行筛选前，总共3176条数据。（就是至少有一个表又该电影信息，都会被记录下来）

任务：要预测前十四天的票房。有两种筛选数据的方法：
1. 预测总票房，然后同时拟合出票房分布曲线，根据百分比预测出前十四天的票房。
- 优点：样本数比较多，2802
- 缺点：两个误差。

2. 直接根据training data里面的第十四天票房作为target value进行预测。
- 优点：只有一个训练误差
- 缺点：训练样本变少了，1141

---------------------------------------------------------------------------

### 筛选data

两个不同任务对数据筛选的要求：
- 主要是totalbox和release date，合并后二者缺一那条数据直接删除不用。
- type和relation表中的数据，有则使用，没有则不用。
- 第一个任务：totalbox和release date以metadata表格为主，box表格为副。
  第二个任务：选取box表格中第14天total box的数据；此外以box表格为主，metadata表格为副，获取release date。

表格里每个feature的具体用法：
1. type（metadata）:
- 不作为筛选根据。
- training data里面有，但是test data里面没有。选模型的时候，training要注意是否加training data中的type。
- training data里面有些type缺失，没关系。

2. 电影名（metadata，box,relation）
- 不作为筛选根据。
- metadata和box中，共存在2873个电影名。全部使用爬虫获得了百度中对应电影名的搜索量。
- relation中存在但是metadata或者box里面不存在的话，直接删除不用，因为这些电影没有totalbox数据，无法作为训练数据，就不用爬虫爬了。
- 电影名字本身应该不能怎么利用。
- 脑洞大点：分析名字字数，用字规律对票房的影响

3. release date（metadata，box）
- 作为筛选根据之一。
- box表中的release date，第0天表示提前放映，同一个电影拥有很多个第0天。现在改用box的第1天作为首映日。
- 在第一种方法中，优先使用metadata中的数据。其次使用box里面的第一天。
- 在第二种方法中，选取box表格中第14天total box的数据；此外以box表格为主，metadata表格为副，获取release date。
- 缺失的处理方法：只要合并后这一项有缺失，当前处理方法会把这一整条数据去掉。

4. totalbox（metadata，box）
- 两个表格的totalbox有部分值相差比较大。
  筛选前共有有3176个电影，其中box表格和metadata表格中含有box信息。
  经过统计，1837个是至少有一个totalbox是缺失的，在这1837个中两个都空缺的373个。
  两个表中都有totalbox，且误差小于10%的有1181个，超过10%的有104个。
  对于空缺的数据，暂时用0来补充。

- 该怎么使用这些数据：
1. 使用二者的最大值
2. 在第一种方法中，优先使用metadata中的数据。其次使用box里面最后一天的box数据；在第二种方法中，优先使用box里面最后一天的box数据。其次使用metadata中的数据。

- totalbox两者都缺失时:knn / 删除整行
  当前：当前处理方法会把这一整条数据去掉。

5. relation(relation)
- training data里面可能缺失，没关系。

* 当前采取的手段更多是删除，而不是补充空缺值。

---------------------------------------------------------------------------

### 生成模型直接使用的数据格式

上一步针对两个不同任务生成任务生成大小不一样的数据集，但是两个数据集中单行数据的格式是一致的。
因此下面的步骤，两个数据集都适用。

注意：可能同一个人在不同feature中同时出现。
            如：冯小刚有可能为演员和导演，则计算冯小刚作为导演的平均票房跟冯小刚作为演员的平均票房是分开的。

###### A：对staff的处理：
0. 每个categorical feature展开，有则为1，没有为0。每个value当一个feature，如有冯小刚则在对应列上为1，没有为0。
1. 每个feature用平均票房作为value。
    如一部电影的演员有三个，则将这三个演员的平均票房作为演员这个feature的value。
2. 与上一个类似，但是平均票房改成平均百度搜索量。
3. 为每个feature中的人按照其搜索量排名，取出前k个作为k个feature。
    如：设定取前三个，则电影x的演员中搜索量排名前三的是a,b,c，则把a,b,c的搜索量当做三个feature。
            同样，制作人，导演，制作，发行用同样方法。
     一份数据共用一个k
4. 与上一个类似，但是使用的不是搜索量排名，而是每个人的参与电影数量进行排名。
    排序后取每一个人的平均票房作为value。
5. 与上一个类似，但是使用每个人的总票房排名，而且挑选后取每一个人的总票房作为value。
6. 与上一个类似，但是使用每个人的平均票房排名，而且挑选后取每一个人的平均票房作为value。
7. 为每个feature进行kmeans聚类，然后用每一类作为一个feature，feature的value为0/1，电影里面有出现这个类别的人则取1，没有取0。
    目前做了三次聚类，每词聚类各个feature的cluster数如下：
feature演员导演制作人制作发行cluster数255555cluster数5010101010cluster数7515151515

8. 为每个feature进行kmeans聚类，然后用每一类作为一个feature，feature的value为该电影中含有该类别的staff人数。

###### B：对日期的处理
1. 取月份，展开成12个0/1取值的feature

###### C：电影搜索量
1. 该电影的百度搜索量

总结：上面列举了每个feature的处理方法，然后在生成数据文件时，用编号表示使用哪个方法。
            如：A1B1C1表示使用了A的第一个方法，B的第一个方法，C的第一个方法，然后合在一起生成一个表格。

-------------------------------------------------------------------------

### 模型

1. knn。距离为曼哈顿距离
2. linear regression
3. svr
4. multilayer perceptron
5. xgboost regression

有待挖掘&调参

