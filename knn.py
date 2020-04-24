import numpy as np

#读取
fo1 = open("iris.data",mode="r")
fo2 = open("bezdekIris.data",mode="r")
list=[]
list2=[]
for line in fo1.readlines():               #依次读取每行
    line = line.strip()                    #去掉每行头尾空白
    list.append(line)
for line in fo2.readlines():               #依次读取每行
    line = line.strip()                    #去掉每行头尾空白
    list2.append(line)

#距离
def distance(d1,d2):
    res = 0
    for key in range(4):
        res += (float(d1[key]) - float(d2[key])) ** 2

    return res ** 0.5

#KNN
k=10
res=[]
def knn(data):
    for line in range(len(list)-1):

        tran=list[line].split(',')

        c={"category":tran[4],"distance":distance(tran,data)}

        res.append(c)

    res3=sorted(res, key=lambda item: item["distance"],reverse = False)  # 由近到远排序
    # 取前K个值

    res2 = res3[0:k]  # 切片

    # 加权平均(category是最终判据)
    result = {'Iris-setosa': 0, 'Iris-versicolor': 0,'Iris-virginica':0}  # 赋值初值
    # 总长度
    sum_dist = 0  # 计算总长度

    for r1 in res2:
        sum_dist += r1['distance']  # for循环计算总长度
    print(sum_dist)
    # 逐个分类加和
    for r2 in res2:
        result[r2["category"]] += 1- r2["distance"] / sum_dist  # 计算每个结果的加权平均值


    if (result['Iris-setosa'] > result['Iris-versicolor'])and(result['Iris-setosa'] > result['Iris-virginica']):  # 输出
        return 'Iris-setosa'
    elif (result['Iris-versicolor'] > result['Iris-setosa'])and(result['Iris-versicolor'] > result['Iris-virginica']):
        return 'Iris-versicolor'
    else:
        return'Iris-virginica'



#----------------------------------------------------------------------

correct = 0
for line in range(len(list2)-1):
    test = list2[line].split(',')
                                        # 遍历
    result = test[4]
    result2 = knn(test)

    if result == result2:  # 如果判断正确则加一
        correct = correct + 1;

print(str(correct/(len(list)-1)))  # 最后打印正确率


fo1.close()