#coding=utf8
def loadDataSet():
    return [['A','B','C','D'],['B','D','E','F'],['B','C','D'],['A','B','C','D','E','F'],['A','C','F'],['B','C','F'],['A','C','D'],['A','B','C','D','G'],['A','B','D','G']]

def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return map(frozenset,C1)


def scanD(D,Ck,minSupport):
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if not ssCnt.has_key(can): ssCnt[can] = 1
                else: ssCnt[can] +=1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key]
        if support >= minSupport:
            retList.insert(0,key)
        supportData[key] = support
    return retList,supportData

def aprioriGen(Lk,k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1,lenLk):
            L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]
            L1.sort(); L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])
    return retList

def apriori(dataSet,minSupport):
    C1 = createC1(dataSet)
    D = map(set,dataSet)
    L1,supportData = scanD(D,C1,minSupport)
    L = [L1]
    k = 2
    while (len(L[k-2])>0):
        Ck = aprioriGen(L[k-2],k)
        Lk, supK = scanD(D,Ck,minSupport)
        supportData.update(supK)
        L.append(Lk)
        k +=1
    return  L,supportData

def generateRules(L,supportData,minConf,filepath):
    bigRuleList = []
    for i in range(1,len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if (i>1):
                rulesFromConseq(freqSet,H1,supportData,bigRuleList,minConf,filepath)
            else:
                calcConf(freqSet,H1,supportData,bigRuleList,minConf,filepath)
    # return bigRuleList

def calcConf(freqSet, H, supportData, br1, minConf,filepath):
    prunedH = []
    f = open(filepath, 'a')
    for conseq in H:
        #计算可信度
        conf = float(supportData[freqSet]) / float(supportData[freqSet-conseq])
        if (conf >= minConf):
            print freqSet-conseq,'-->',conseq,'conf:',conf
            f.writelines(str(freqSet-conseq) + '-->' + str(conseq) + 'conf:' + str(conf) + '\n')
            br1.append((freqSet-conseq,conseq,conf))
            prunedH.append(conseq)
    f.close()
    return prunedH

def rulesFromConseq(freqSet, H, supportData, br1, minConf,filepath):
    m = len(H[0])
    if (len(freqSet) > (m+1)):
        if (m==1):
            Hmp1 = calcConf(freqSet, H, supportData,br1, minConf,filepath)

        Hmp1 = aprioriGen(H,m+1)
        Hmp1 = calcConf(freqSet, Hmp1, supportData,br1, minConf,filepath)
        if (len(Hmp1) > 1):
            rulesFromConseq(freqSet, Hmp1, supportData, br1, minConf,filepath)










