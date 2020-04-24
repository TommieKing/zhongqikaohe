from numpy import *
import matplotlib.pyplot as plt
olderr = seterr(all='ignore')

#读取
fo1 = open("iris.data", mode="r")
list1 = []
for line in fo1.readlines():  # 依次读取每行
    line = line.strip()  # 去掉每行头尾空白
    list1.append(line)#将文件中内容储存到list1

dataSet = []
for r in range(len(list1) - 1):
    tran = list1[r].split(',')#遍历list1，去掉‘，’
    fltLine = list(map(float, tran[:4]))#只取数据
    dataSet.append(fltLine)#将切片好的数据存到dataSet


# 计算两个向量的欧式距离（可根据场景选择）
def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2)))  # la.norm(vecA-vecB)


# 为给定数据集构建一个包含 k 个随机质心的集合。随机质心必须要在整个数据集的边界之内，
# 这可以通过找到数据集每一维的最小和最大值来完成。然后生成 0~1.0 之间的随机数并通过取值范围和最小值，以便确保随机点在数据的边界之内。
def randCent(dataMat, k):
    n = shape(dataMat)[1]  # 列的数量
    centroids = mat(zeros((k, n)))  # 创建k个质心矩阵
    for j in range(n):  # 创建随机簇质心，并且在每一维的边界内
        minJ = min(dataMat[:, j])  # 最小值
        rangeJ = float(max(dataMat[:, j]) - minJ)  # 范围 = 最大值 - 最小值
        centroids[:, j] = mat(minJ + rangeJ * random.rand(k, 1))  # 随机生成
    return centroids


# k-means
def kMeans(dataMat, k, distMeas=distEclud, createCent=randCent):
    m = shape(dataMat)[0]  # 行数
    clusterAssment = mat(zeros((m, 2)))  # 创建一个与 dataMat 行数一样，但是有两列的矩阵，用来保存簇分配结果
    centroids = createCent(dataMat, k)  # 创建质心，随机k个质心
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):  # 循环每一个数据点并分配到最近的质心中去
            minDist = inf
            minIndex = -1
            for j in range(k):
                distJI = distMeas(centroids[j, :],dataMat[i, :])  # 计算数据点到质心的距离
                if distJI < minDist:  # 如果距离比 minDist（最小距离）还小，更新 minDist（最小距离）和最小质心的 index（索引）
                    minDist = distJI
                    minIndex = j
            if clusterAssment[i, 0] != minIndex:  # 簇分配结果改变
                clusterChanged = True  # 簇改变
                clusterAssment[ i, :] = minIndex, minDist  # 更新簇分配结果为最小质心的 index（索引），minDist（最小距离）
        # print(centroids)
        for cent in range(k):  # 更新质心
            ptsInClust = dataMat[nonzero(clusterAssment[:, 0].A == cent)[0]]  # 获取该簇中的所有点
            centroids[cent, :] = mean(ptsInClust, axis=0)  # 将质心修改为簇中所有点的平均值，mean 就是求平均值的
    return centroids, clusterAssment





def testBasicFunc():
    # 加载测试数据集
    dataMat = dataSet
    dataMat = array(dataMat)
    # 测试 randCent() 函数是否正常运行。
    # 首先，先看一下矩阵中的最大值与最小值
    print('min(dataMat[:, 0])=', min(dataMat[:, 0]))
    print('min(dataMat[:, 1])=', min(dataMat[:, 1]))
    print('max(dataMat[:, 1])=', max(dataMat[:, 1]))
    print('max(dataMat[:, 0])=', max(dataMat[:, 0]))

    # 然后看看 randCent() 函数能否生成 min 到 max 之间的值
    print('randCent(dataMat, 2)=', randCent(dataMat, 2))

    # 最后测试一下距离计算方法
    print(' distEclud(dataMat[0], dataMat[1])=', distEclud(dataMat[0], dataMat[1]))
# testBasicFunc()


def testKMeans():
    # 加载测试数据集
    dataMat = dataSet
    dataMat = array(dataMat)
    # 该算法会创建k个质心，然后将每个点分配到最近的质心，再重新计算质心。
    # 这个过程重复数次，知道数据点的簇分配结果不再改变位置。
    # 运行结果（多次运行结果可能会不一样，可以试试，原因为随机质心的影响，但总的结果是对的， 因为数据足够相似）
    myCentroids, clustAssing = kMeans(dataMat, 3)

    print('centroids=', myCentroids)


testKMeans()
testKMeans()
testKMeans()
