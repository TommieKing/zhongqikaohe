
from numpy import *


#读取
fo1 = open("agaricus-lepiota.data", mode="r")
list1 = []
dataSet=[]
for line in fo1.readlines():  # 依次读取每行
    line = line.strip()  # 去掉每行头尾空白
    list1.append(line)#将文件中内容储存到list1


for r in range(len(list1) - 1):
    tran = list1[r].split(',')#遍历list1，去掉‘，’
    dataSet.append(tran)#将数据存到dataSet


# 创建集合 C1。即对 dataSet 进行去重，排序，放入 list 中，然后转换所有的元素为 frozenset
def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                # 遍历所有的元素，如果不在 C1 出现过，那么就 append
                C1.append([item])
    C1.sort()
    # frozenset 表示冻结的 set 集合，元素无改变；可以把它当字典的 key 来使用

    C1=list(map(frozenset, C1))
    return C1
# c=createC1(dataSet)
# print(c)
# 计算候选数据集 CK 在数据集 D 中的支持度，并返回支持度大于最小支持度（minSupport）的数据
def scanD(D, Ck, minSupport):

    ssCnt = {}# ssCnt 临时存放侯选数据集 Ck 的频率. 例如: a->10, b->5, c->8
    for tid in D:#数据集 D
        for can in Ck:#ck候选数据集
                                      # s.issubset(t)  测试是否 s 中的每一个元素都在 t 中
            if can.issubset(tid):
                if not can in ssCnt:
                    # has_key() 函数用于判断键是否存在于字典中，如果键在字典dict里返回true，否则返回false。
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    numItems = float(len(D))  # numItems数据集 D 的数量
    retList = []
    supportData = {}
    for key in ssCnt:# ssCnt 临时存放侯选数据集 Ck 的频率
        # 支持度 = 候选项（key）出现的次数 / 所有数据集的数量
        support = ssCnt[key] / numItems
        if support >= minSupport:#最小支持度（minSupport）
                                        # 在 retList 的首位插入元素，只存储支持度满足频繁项集的值
            retList.insert(0, key)
                                         # 存储所有的候选项（key）和对应的支持度（support）
        supportData[key] = support
    return retList, supportData   #retList 支持度大于 minSupport 的数集    supportData 候选项集支持度数据
# scanD(D, Ck, 0.5)

# 输入频繁项集列表 Lk 与返回的元素个数 k，然后输出所有可能的候选项集 Ck
def aprioriGen(Lk, k):

    # 输入频繁项集列表 Lk 与返回的元素个数 k，然后输出所有可能的候选项集 Ck
    retList = []
    lenLk = len(Lk)#Lk频繁项集，lenLk频繁项集长度
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            L1 = list(Lk[i])[: k - 2]
            L2 = list(Lk[j])[: k - 2]

# 注意其生成的过程中，首选对每个项集按元素排序，然后每次比较两个项集，只有在前k-1项相同时才将这两项合并。这样做是因为函数并非要两两合并各个集合，
# 那样生成的集合并非都是k+1项的。在限制项数为k+1的前提下，只有在前k-1项相同、最后一项不相同的情况下合并才为所需要的新候选项集。
            L1.sort()
            L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])
    return retList


# 找出数据集 dataSet 中支持度 >= 最小支持度的候选项集以及它们的支持度。即我们的频繁项集。
def apriori(dataSet, minSupport=0.5):
    # C1 即对 dataSet 进行去重，排序，放入 list 中，然后转换所有的元素为 frozenset
    C1 = createC1(dataSet)

    # 对每一行进行 set 转换，然后存放到集合中
    D = list(map(set, dataSet))
    # print('D=', D)
    # 计算候选数据集 C1 在数据集 D 中的支持度，并返回支持度大于 minSupport 的数据
    L1, supportData = scanD(D, C1, minSupport)# 计算候选数据集 C1 在数据集 D 中的支持度，并返回支持度大于最小支持度（minSupport）的数据
    # L 加了一层 list, L 一共 2 层 list，方便以后调用不同大小的数据集
    # print(L1)
    L = [L1]
    # print(L[0])
    k = 2
    # 判断 L 的第 k-2 项的数据长度是否 > 0。
    while (len(L[k - 2]) > 0):
        # print 'k=', k, L, L[k-2]
        Ck = aprioriGen(L[k - 2],k)  # 输入频繁项集列表 Lk 与返回的元素个数 k，然后输出所有可能的候选项集 Ck

        Lk, supK = scanD(D, Ck, minSupport)  # 继续筛选满足最小支持度的数据集
        # 保存所有候选项集的支持度，如果字典没有，就追加元素，如果有，就更新元素
        supportData.update(supK)#更新支持度
        if len(Lk) == 0:#如果lk长度为0，则证明再没有满足符合最小支持度的数据集，则退出循环
            break

        L.append(Lk)#L中添加生成的数据集
        k += 1#一次循环后，k值加一，生成长度更大的数据集

    return L, supportData  # 返回频繁数集和他们的支持度集合

# 计算可信度（confidence）
def calcConf(freqSet, H, supportData, brl, minConf=0.7):

        # freqSet 频繁项集中的元素，例如: frozenset([1, 3])
        # H 频繁项集中的元素的集合，例如: [frozenset([1]), frozenset([3])]
        # supportData 所有元素的支持度的字典
        # brl 关联规则列表的空数组
        # minConf 最小可信度
        # prunedH 记录 可信度大于阈值的集合

    # 记录可信度大于最小可信度（minConf）的集合
    prunedH = []
    for conseq in H:  # 假设 频繁项集中的元素freqSet = frozenset([1, 3]), 频繁项集中的元素的集合H = [frozenset([1]), frozenset([3])]，
        # 那么现在需要求出 frozenset([1]) -> frozenset([3]) 的可信度和 frozenset([3]) -> frozenset([1]) 的可信度
        conf = supportData[freqSet] / supportData[freqSet - conseq]
        # 支持度定义: a -> b = support(a | b) / support(a). 假设  freqSet = frozenset([1, 3]),
        # conseq = [frozenset([1])]，那么 frozenset([1]) 至 frozenset([3]) 的可信度为 = support(a | b) / support(a) = supportData[freqSet]/supportData[freqSet-conseq] = supportData[frozenset([1, 3])] / supportData[frozenset([1])]
        if conf >= minConf:
            # 只要买了 freqSet-conseq 集合，一定会买 conseq 集合（freqSet-conseq 集合和 conseq集合 是全集）
            print(freqSet - conseq, '-->', conseq, 'conf:', conf)
            brl.append((freqSet - conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH

# 递归计算频繁项集的规则
def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):

        # freqSet 频繁项集中的元素，例如: frozenset([2, 3, 5])
        # H 频繁项集中的元素的集合，例如: [frozenset([2]), frozenset([3]), frozenset([5])]
        # supportData 所有元素的支持度的字典
        # brl 关联规则列表的数组
        # minConf 最小可信度
    # H[0] 是 freqSet 的元素组合的第一个元素，并且 H 中所有元素的长度都一样，长度由 aprioriGen(H, m+1) 这里的 m + 1 来控制
    # 该函数递归时，H[0] 的长度从 1 开始增长 1 2 3 ...
    # 假设 freqSet = frozenset([2, 3, 5]), H = [frozenset([2]), frozenset([3]), frozenset([5])]
    # 那么 m = len(H[0]) 的递归的值依次为 1 2
    # 在 m = 2 时, 跳出该递归。假设再递归一次，那么 H[0] = frozenset([2, 3, 5])，freqSet = frozenset([2, 3, 5]) ，
    # 没必要再计算 freqSet 与 H[0] 的关联规则了。
    m = len(H[0])
    if (len(freqSet) > (m + 1)):
        # print 'freqSet******************', len(freqSet), m + 1, freqSet, H, H[0]
        # 生成 m+1 个长度的所有可能的 H 中的组合，假设 H = [frozenset([2]), frozenset([3]), frozenset([5])]
        # 第一次递归调用时生成 [frozenset([2, 3]), frozenset([2, 5]), frozenset([3, 5])]
        # 第二次 。。。没有第二次，递归条件判断时已经退出了
        Hmp1 = aprioriGen(H, m+1)
        # 返回可信度大于最小可信度的集合
        Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
        print('Hmp1=', Hmp1)
        print('len(Hmp1)=', len(Hmp1), 'len(freqSet)=', len(freqSet))
        # 计算可信度后，还有数据大于最小可信度的话，那么继续递归调用，否则跳出递归
        if (len(Hmp1) > 1):

            rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)

# 生成关联规则
def generateRules(L, supportData, minConf=0.7):

       #   L 频繁项集列表
       # supportData 频繁项集支持度的字典
       # minConf 最小置信度

    bigRuleList = []
    # 假设 L = [[frozenset([1]), frozenset([3]), frozenset([2]), frozenset([5])], [frozenset([1, 3]),frozenset([2, 5]), frozenset([2, 3]), frozenset([3, 5])], [frozenset([2, 3, 5])]]
    for i in range(1, len(L)):
        # 获取频繁项集中每个组合的所有元素
        for freqSet in L[i]:
            # 假设：freqSet= frozenset([1, 3]), H1=[frozenset([1]), frozenset([3])]
            # 组合总的元素并遍历子元素，并转化为 frozenset 集合，再存放到 list 列表中
            H1 = [frozenset([item]) for item in freqSet]
            # 2 个的组合，走 else, 2 个以上的组合，走 if
            if (i > 1):
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList # 可信度规则列表（关于 (A->B+置信度) 3个字段的组合）


def main():

    L, supportData = apriori(dataSet,minSupport=0.3)


    # for item in L[1]:
    #     if item.intersection('e'):
    #         print(item)
    #
    # for item in L[2]:
    #     if item.intersection('e'):
    #         print(item)


main()