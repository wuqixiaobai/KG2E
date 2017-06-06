#-*- coding:utf-8 –*-
from random import uniform, sample
from numpy import *
from copy import deepcopy
import test

class TransE:
    def __init__(self, DBentityList, DBrelationList, DBtripleList, FBentityList, FBrelationList, FBtripleList, margin = 1, learingRate = 0.001, dim = 0, L1 = True, weight=5):
        self.margin = margin
        self.learingRate = learingRate
        self.dim = dim #向量维度
        self.DBentityList = DBentityList#一开始，entityList是entity的list；初始化后，变为字典，key是entity，values是其向量（使用narray）。
        self.DBrelationList = DBrelationList#理由同上
        self.DBtripleList = DBtripleList#理由同上
        self.FBentityList = FBentityList#一开始，entityList是entity的list；初始化后，变为字典，key是entity，values是其向量（使用narray）。
        self.FBrelationList = FBrelationList#理由同上
        self.FBtripleList = FBtripleList#理由同上
        self.loss = 0
        self.L1 = L1
        self.weight=weight#SameAs关系权重

    def initialize(self):
        '''
        初始化向量
        '''
        DBentityVectorList = {} #实体vector字典
        DBrelationVectorList = {} #关系vector字典
        for entity in self.DBentityList:
            n = 0
            entityVector = []
            while n < self.dim:
                ram = init(self.dim) #初始化实体的vector的范围
                entityVector.append(ram)
                n += 1
            DBentityVector = norm(entityVector)#归一化
            DBentityVectorList[entity] = entityVector #词典的key 是实体，value是向量
        print("DBentityVector初始化完成，数量是%d"%len(DBentityVectorList))
        for relation in self.DBrelationList:
            n = 0
            relationVector = []
            while n < self.dim:
                ram = init(self.dim)#初始化的范围
                relationVector.append(ram)
                n += 1
            DBrelationVector = norm(relationVector)#归一化
            DBrelationVectorList[relation] = relationVector
        print("DBrelationVectorList初始化完成，数量是%d"%len(DBrelationVectorList))
        self.DBentityList = DBentityVectorList
        self.DBrelationList = DBrelationVectorList
        FBentityVectorList = {} #实体vector字典
        FBrelationVectorList = {} #关系vector字典
        for entity in self.FBentityList:
            n = 0
            entityVector = []
            while n < self.dim:
                ram = init(self.dim) #初始化实体的vector的范围
                entityVector.append(ram)
                n += 1
            FBentityVector = norm(entityVector)#归一化
            FBentityVectorList[entity] = entityVector #词典的key 是实体，value是向量
        print("FBentityVector初始化完成，数量是%d"%len(FBentityVectorList))
        for relation in self.FBrelationList:
            n = 0
            relationVector = []
            while n < self.dim:
                ram = init(self.dim)#初始化的范围
                relationVector.append(ram)
                n += 1
            FBrelationVector = norm(relationVector)#归一化
            FBrelationVectorList[relation] = relationVector
        print("FBrelationVectorList初始化完成，数量是%d"%len(FBrelationVectorList))
        self.FBentityList = FBentityVectorList
        self.FBrelationList = FBrelationVectorList
    def transE(self, cI = 20):
        print("训练开始")
        for cycleIndex in range(cI):  #随机梯度下降
            S_DBbatch = self.getSample(150,"DB") #SGD的DBBatch
            S_FBbatch=self.getSample(150,"FB")#SGD的FBBatch
            T_DBbatch = []#元组对（原三元组，打碎的三元组）的列表 ：{((h,r,t),(h',r,t'))}
            T_FBbatch = []#元组对（原三元组，打碎的三元组）的列表 ：{((h,r,t),(h',r,t'))}
            for sbatch in S_DBbatch:
                Corrupted_DBTriplet = (sbatch, self.getCorruptedTriplet(sbatch,"DB")) #每一个元素都是turple
                if(Corrupted_DBTriplet not in T_DBbatch):
                    T_DBbatch.append(Corrupted_DBTriplet)
            for sbatch in S_FBbatch:
                Corrupted_FBTriplet = (sbatch, self.getCorruptedTriplet(sbatch,"FB")) #每一个元素都是turple
                if(Corrupted_DBTriplet not in T_FBbatch):
                    T_FBbatch.append(Corrupted_FBTriplet)
            self.update(T_DBbatch,T_FBbatch) #包含了DB与FB各包含了150个正确，与错误的三元组
            if cycleIndex % 100 == 0:
                print("第%d次循环"%cycleIndex)
                print(self.loss)
                self.writeRelationVector("FB_relationVector.txt")
                self.writeEntilyVector("FB_entityVector.txt")
                self.loss = 0

    def getSample(self, size,index):
        if index="DB":
            return sample(self.DBtripleList, size)
        else:
            return sample(self.FBtripleList, size)

    def getCorruptedTriplet(self, triplet, index):
        '''
        training triplets with either the head or tail replaced by a random entity (but not both at the same time)
        :param triplet:
        :return corruptedTriplet:
        '''
        i = uniform(-1, 1)
        if i < 0:#小于0，打坏三元组的第一项
            while True:
                if index="DB":
                    entityTemp = sample(self.DBentityList.keys(), 1)[0]
                else:
                    entityTemp = sample(self.FBentityList.keys(), 1)[0]
                if entityTemp != triplet[0]:
                    break
            corruptedTriplet = (entityTemp, triplet[1], triplet[2])
        else:#大于等于0，打坏三元组的第二项
            while True:
                if index="DB":
                    entityTemp = sample(self.DBentityList.keys(), 1)[0]
                else:
                    entityTemp = sample(self.FBentityList.keys(), 1)[0]
                if entityTemp != triplet[1]:
                    break
            corruptedTriplet = (triplet[0], entityTemp, triplet[2])
        return corruptedTriplet

    def update(self, T_DBbatch,T_FBbatch):
        CP_DBEntityList = deepcopy(self.DBentityList)  #是一个字典，key为实体的名字，value是实体的vector
        CP_DBRelationList = deepcopy(self.DBrelationList)
        CP_FBEntityList = deepcopy(self.FBentityList)  #是一个字典，key为实体的名字，value是实体的vector
        CP_FBRelationList = deepcopy(self.FBrelationList)
        for Corrupted_FBTriplet in T_FBbatch:
            head_FBEntityVector = CP_FBEntityList[Corrupted_FBTriplet[0][0]]#tripletWithCorruptedTriplet是原三元组和打碎的三元组的元组tuple
            tail_FBEntityVector = CP_FBEntityList[Corrupted_FBTriplet[0][1]]
            FBrelationVector = CP_FBEntityList[Corrupted_FBTriplet[0][2]]
            head_FBCorruptedTriplet = CP_FBEntityList[Corrupted_FBTriplet[1][0]]
            tail_FBCorruptedTriplet = CP_FBEntityList[Corrupted_FBTriplet[1][1]]
            head_FBBefore = self.FBentityList[Corrupted_FBTriplet[0][0]]#tripletWithCorruptedTriplet是原三元组和打碎的三元组的元组tuple
            tail_FBBefore= self.FBentityList[Corrupted_FBTriplet[0][1]]
            relation_FBBefore= self.FBrelationList[Corrupted_FBTriplet[0][2]]
            head_FBCorruptedBefore= self.FBentityList[Corrupted_FBTriplet[1][0]]
            tail_FBCorruptedBefore = self.FBentityList[Corrupted_FBTriplet[1][1]]
            if self.L1:
                distFB = distanceL1(head_FBBefore, tail_FBBefore, relation_FBBefore)
                dist_FBCorrupt= distanceL1(head_FBCorruptedBefore, tail_FBCorruptedBefore, relation_FBBefore)
            else:
                distFB = distanceL2(head_FBBefore, tail_FBBefore, relation_FBBefore)
                dist_FBCorrupt = distanceL2(head_FBCorruptedBefore, tail_FBCorruptedBefore ,  relation_FBBefore)
            eg = self.margin + distTriplet - distCorruptedTriplet
            if eg > 0: #[function]+ 是一个取正值的函数
                self.loss += eg
                if self.L1:
                    tempPositive = 2 * self.learingRate * (tailEntityVectorBeforeBatch - headEntityVectorBeforeBatch - relationVectorBeforeBatch)
                    tempNegtative = 2 * self.learingRate * (tailEntityVectorWithCorruptedTripletBeforeBatch - headEntityVectorWithCorruptedTripletBeforeBatch - relationVectorBeforeBatch)
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
                    tempPositive = 2 * self.learingRate * (tailEntityVectorBeforeBatch - headEntityVectorBeforeBatch - relationVectorBeforeBatch)
                    tempNegtative = 2 * self.learingRate * (tailEntityVectorWithCorruptedTripletBeforeBatch - headEntityVectorWithCorruptedTripletBeforeBatch - relationVectorBeforeBatch)

                headEntityVector = headEntityVector + tempPositive
                tailEntityVector = tailEntityVector - tempPositive
                relationVector = relationVector + tempPositive - tempNegtative
                headEntityVectorWithCorruptedTriplet = headEntityVectorWithCorruptedTriplet - tempNegtative
                tailEntityVectorWithCorruptedTriplet = tailEntityVectorWithCorruptedTriplet + tempNegtative

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
    """
    dirEntity = "/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/entity2id.txt"
    entityIdNum, entityList = openDetailsAndId(dirEntity)
    dirRelation = "/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/relation2id.txt"
    relationIdNum, relationList = openDetailsAndId(dirRelation)
    dirTrain = "/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/train.txt"
    tripleNum, tripleList = openTrain(dirTrain)
    print("打开TransE")
    transE = TransE(entityList,relationList,tripleList, margin=2, dim = 50)
    print("TranE初始化")
    transE.initialize()
    transE.transE(10000)
    transE.writeRelationVector("/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/relationVector.txt")
    transE.writeEntilyVector("/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/entityVector.txt")
    """
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
