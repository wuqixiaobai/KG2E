#-*- coding:utf-8 –*-
from random import uniform, sample
from numpy import *
from copy import deepcopy
import test

class TransE:
    def __init__(self, entityList, relationList, tripleList, margin = 1, learingRate = 0.001, dim = 10, L1 = True):
        self.margin = margin
        self.learingRate = learingRate
        self.dim = dim #向量维度
        self.entityList = entityList#一开始，entityList是entity的list；初始化后，变为字典，key是entity，values是其向量（使用narray）。
        self.relationList = relationList#理由同上
        self.tripleList = tripleList#理由同上
        self.loss = 0
        self.L1 = L1

    def initialize(self):
        '''
        初始化向量
        '''
        entityVectorList = {} #实体vector字典
        relationVectorList = {} #关系vector字典
        for entity in self.entityList:
            n = 0
            entityVector = []
            while n < self.dim:
                ram = init(self.dim) #初始化实体的vector的范围
                entityVector.append(ram)
                n += 1
            entityVector = norm(entityVector)#归一化
            entityVectorList[entity] = entityVector #词典的key 是实体，value是向量
        print("entityVector初始化完成，数量是%d"%len(entityVectorList))
        for relation in self. relationList:
            n = 0
            relationVector = []
            while n < self.dim:
                ram = init(self.dim)#初始化的范围
                relationVector.append(ram)
                n += 1
            relationVector = norm(relationVector)#归一化
            relationVectorList[relation] = relationVector
        print("relationVectorList初始化完成，数量是%d"%len(relationVectorList))
        self.entityList = entityVectorList
        self.relationList = relationVectorList

    def transE(self, cI = 20):
        print("训练开始")
        for cycleIndex in range(cI):
            Sbatch = self.getSample(1500) #SGD的Batch
            Tbatch = []#元组对（原三元组，打碎的三元组）的列表 ：{((h,r,t),(h',r,t'))}
            for sbatch in Sbatch:
                tripletWithCorruptedTriplet = (sbatch, self.getCorruptedTriplet(sbatch)) #每一个元素都是turple
                if(tripletWithCorruptedTriplet not in Tbatch):
                    Tbatch.append(tripletWithCorruptedTriplet)
            self.update(Tbatch) #包含了150个正确，与错误的三元组
            print("第%d次循环"%cycleIndex)
            print(self.loss)
            self.loss = 0

    def getSample(self, size):
        return sample(self.tripleList, size)

    def getCorruptedTriplet(self, triplet):
        '''
        training triplets with either the head or tail replaced by a random entity (but not both at the same time)
        :param triplet:
        :return corruptedTriplet:
        '''
        i = uniform(-1, 1)
        if i < 0:#小于0，打坏三元组的第一项
            while True:
                entityTemp = sample(self.entityList.keys(), 1)[0]
                if entityTemp != triplet[0]:
                    break
            corruptedTriplet = (entityTemp, triplet[1], triplet[2])
        else:#大于等于0，打坏三元组的第二项
            while True:
                entityTemp = sample(self.entityList.keys(), 1)[0]
                if entityTemp != triplet[1]:
                    break
            corruptedTriplet = (triplet[0], entityTemp, triplet[2])
        return corruptedTriplet

    def update(self, Tbatch):
        copyEntityList = deepcopy(self.entityList)  #是一个字典，key为实体的名字，value是实体的vector
        copyRelationList = deepcopy(self.relationList)
        for tripletWithCorruptedTriplet in Tbatch:
            headEntityVector = copyEntityList[tripletWithCorruptedTriplet[0][0]]#tripletWithCorruptedTriplet是原三元组和打碎的三元组的元组tuple
            tailEntityVector = copyEntityList[tripletWithCorruptedTriplet[0][1]]
            relationVector = copyRelationList[tripletWithCorruptedTriplet[0][2]]
            headEntityVectorWithCorruptedTriplet = copyEntityList[tripletWithCorruptedTriplet[1][0]]
            tailEntityVectorWithCorruptedTriplet = copyEntityList[tripletWithCorruptedTriplet[1][1]]
            headEntityVectorBeforeBatch = self.entityList[tripletWithCorruptedTriplet[0][0]]#tripletWithCorruptedTriplet是原三元组和打碎的三元组的元组tuple
            tailEntityVectorBeforeBatch = self.entityList[tripletWithCorruptedTriplet[0][1]]
            relationVectorBeforeBatch = self.relationList[tripletWithCorruptedTriplet[0][2]]
            headEntityVectorWithCorruptedTripletBeforeBatch = self.entityList[tripletWithCorruptedTriplet[1][0]]
            tailEntityVectorWithCorruptedTripletBeforeBatch = self.entityList[tripletWithCorruptedTriplet[1][1]]
            if self.L1:
                distTriplet = distanceL1(headEntityVectorBeforeBatch, tailEntityVectorBeforeBatch, relationVectorBeforeBatch)
                distCorruptedTriplet = distanceL1(headEntityVectorWithCorruptedTripletBeforeBatch, tailEntityVectorWithCorruptedTripletBeforeBatch ,  relationVectorBeforeBatch)
            else:
                distTriplet = distanceL2(headEntityVectorBeforeBatch, tailEntityVectorBeforeBatch, relationVectorBeforeBatch)
                distCorruptedTriplet = distanceL2(headEntityVectorWithCorruptedTripletBeforeBatch, tailEntityVectorWithCorruptedTripletBeforeBatch ,  relationVectorBeforeBatch)
            eg = self.margin + distTriplet - distCorruptedTriplet
            if eg > 0: #[function]+ 是一个取正值的函数
                self.loss += eg
                if self.L1:
                    tempPositive = 2 *  (tailEntityVectorBeforeBatch - headEntityVectorBeforeBatch - relationVectorBeforeBatch)
                    tempNegtative = 2 * (tailEntityVectorWithCorruptedTripletBeforeBatch - headEntityVectorWithCorruptedTripletBeforeBatch - relationVectorBeforeBatch)
                    tempPositiveL1 = []
                    tempNegtativeL1 = []
                    for i in range(self.dim):#不知道有没有pythonic的写法（比如列表推倒或者numpy的函数）？
                        if tempPositive[i] >= 0:
                            tempPositiveL1.append(1)
                        else:
                            tempPositiveL1.append(-1)
                        if tempNegtative[i] >= 0:
                            tempNegtativeL1.append(1)
                        else:
                            tempNegtativeL1.append(-1)
                    tempPositive = array(tempPositiveL1)
                    tempNegtative = array(tempNegtativeL1)

                else:
                    tempPositive = 2 *  (tailEntityVectorBeforeBatch - headEntityVectorBeforeBatch - relationVectorBeforeBatch)
                    tempNegtative = 2 * (tailEntityVectorWithCorruptedTripletBeforeBatch - headEntityVectorWithCorruptedTripletBeforeBatch - relationVectorBeforeBatch)

                headEntityVector = headEntityVector +  self.learingRate* tempPositive
                tailEntityVector = tailEntityVector -  self.learingRate*tempPositive
                relationVector = relationVector +  self.learingRate*(tempPositive - tempNegtative)
                headEntityVectorWithCorruptedTriplet = headEntityVectorWithCorruptedTriplet - self.learingRate*tempNegtative
                tailEntityVectorWithCorruptedTriplet = tailEntityVectorWithCorruptedTriplet + self.learingRate*tempNegtative

                #只归一化这几个刚更新的向量，而不是按原论文那些一口气全更新了
                copyEntityList[tripletWithCorruptedTriplet[0][0]] = norm(headEntityVector)
                copyEntityList[tripletWithCorruptedTriplet[0][1]] = norm(tailEntityVector)
                copyRelationList[tripletWithCorruptedTriplet[0][2]] = norm(relationVector)
                copyEntityList[tripletWithCorruptedTriplet[1][0]] = norm(headEntityVectorWithCorruptedTriplet)
                copyEntityList[tripletWithCorruptedTriplet[1][1]] = norm(tailEntityVectorWithCorruptedTriplet)

        self.entityList = copyEntityList
        self.relationList = copyRelationList

    def writeEntilyVector(self, dir):
        print("写入实体")
        entityVectorFile = open(dir, 'w')
        for entity in self.entityList.keys():
            entityVectorFile.write(entity+"\t")
            entityVectorFile.write(str(self.entityList[entity].tolist()))
            entityVectorFile.write("\n")
        entityVectorFile.close()

    def writeRelationVector(self, dir):
        print("写入关系")
        relationVectorFile = open(dir, 'w')
        for relation in self.relationList.keys():
            relationVectorFile.write(relation + "\t")
            relationVectorFile.write(str(self.relationList[relation].tolist()))
            relationVectorFile.write("\n")
        relationVectorFile.close()

def init(dim):
    return uniform(-6/(dim**0.5), 6/(dim**0.5))

def distanceL1(h, t ,r):
    s = h + r - t
    sum = fabs(s).sum()
    return sum

def distanceL2(h, t, r):
    s = h + r - t
    sum = (s*s).sum()
    return sum

def norm(list):
    '''
    归一化
    :param 向量
    :return: 向量的平方和的开方后的向量
    '''
    var = linalg.norm(list)
    i = 0
    while i < len(list):
        list[i] = list[i]/var
        i += 1
    return array(list)

def openDetailsAndId(dir,sp=" "):
    idNum = 0
    list = []
    with open(dir) as file:
        lines = file.readlines()
        for line in lines:
            DetailsAndId = line.strip().split(sp)
            list.append(DetailsAndId[0])
            idNum += 1
    return idNum, list

def openTrain(dir,sp="\t"):
    num = 0
    list = []
    with open(dir) as file:
        lines = file.readlines()
        for line in lines:
            triple = line.strip().split(sp)
            if(len(triple)<3):
                continue
            list.append(tuple(triple))
            num += 1
    return num, list

if __name__ == '__main__':
    dirEntity = "/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/entity2id.txt"
    entityIdNum, entityList = openDetailsAndId(dirEntity)
    dirRelation = "/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/relation2id.txt"
    relationIdNum, relationList = openDetailsAndId(dirRelation)
    dirTrain = "/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/train.txt"
    tripleNum, tripleList = openTrain(dirTrain)
    print(tripleNum)
    print("打开TransE")
    transE = TransE(entityList,relationList,tripleList, margin=2, dim = 20, L1 = True)
    print("TranE初始化")
    transE.initialize()
    transE.transE(5000)
    transE.writeRelationVector("/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/relationVector.txt")
    transE.writeEntilyVector("/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/entityVector.txt")
    print("开始测试")
    dirEntityTest =  "/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/test_Entity.txt"
    EntityTest = test.openD(dirEntityTest)
    print("Read Entity")
    dirRelationTest = "/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/test_Relation.txt"
    RelationTest = test.openD(dirRelationTest)
    print("Read Relation")
    dirEntityVector = "/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/entityVector.txt"
    entityVectorList, entityList = test.loadData(dirEntityVector)
    print("Read EntitVector")
    dirRelationVector = "/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/relationVector.txt"
    relationVectorList, relationList = test.loadData(dirRelationVector)
    print("Read RelationVector")
    testHeadRaw = test.Test(entityList, entityVectorList, relationList, relationVectorList, EntityTest, RelationTest)
    testHeadRaw.getRank()
    print("MeanRank of HeadRaw is %f"%(testHeadRaw.getMeanRank()))
    testHeadRaw.writeRank("/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/" + "testHeadRaw" + ".txt")
    """
    testHeadRaw.getRelationRank()
    print("MeanRank of Relation is %f"%(testHeadRaw.getMeanRank()))
    testHeadRaw.writeRank("/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/" + "testRelationRaw" + ".txt")
    """
    testTailRaw = test.Test(entityList, entityVectorList, relationList, relationVectorList, EntityTest, RelationTest, label = "tail")
    testTailRaw.getRank()
    print("MeanRank of HeadRaw is %f"%(testHeadRaw.getMeanRank()))
    print("MeanRank of TailRaw is %f"%(testTailRaw.getMeanRank()))
    testTailRaw.writeRank("/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/" + "testTailRaw" + ".txt")
    print("Done")
