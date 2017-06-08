#-*- coding:utf-8 –*-
from random import uniform, sample
from numpy import *
from copy import deepcopy
import MGTest

class TransE:
    def __init__(self, DBentityList, DBrelationList, DBtripleList, FBentityList, FBrelationList, FBtripleList, SameAs, margin = 1, learingRate = 0.001, dim = 10, L1 = True, weight=5):
        self.margin = margin
        self.learingRate = learingRate
        self.dim = dim #向量维度
        self.DBentityList = DBentityList#一开始，entityList是entity的list；初始化后，变为字典，key是entity，values是其向量（使用narray）。
        self.DBrelationList = DBrelationList#理由同上
        self.DBtripleList = DBtripleList#理由同上
        self.FBentityList = FBentityList#一开始，entityList是entity的list；初始化后，变为字典，key是entity，values是其向量（使用narray）。
        self.FBrelationList = FBrelationList#理由同上
        self.FBtripleList = FBtripleList#理由同上
        self.SameAs=SameAs #存储SameAs关系 FB为key,DB是Value
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
            entityVector = norm(entityVector)#归一化
            DBentityVectorList[entity] = entityVector #词典的key 是实体，value是向量
        print("DBentityVector,number is %d"%len(DBentityVectorList))
        for relation in self.DBrelationList:
            n = 0
            relationVector = []
            while n < self.dim:
                ram = init(self.dim)#初始化的范围
                relationVector.append(ram)
                n += 1
            relationVector = norm(relationVector)#归一化
            DBrelationVectorList[relation] = relationVector
        print("DBrelationVectorList,number is %d"%len(DBrelationVectorList))
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
            entityVector = norm(entityVector)#归一化
            FBentityVectorList[entity] = entityVector #词典的key 是实体，value是向量
        print("FBentityVector,number is %d"%len(FBentityVectorList))
        for relation in self.FBrelationList:
            n = 0
            relationVector = []
            while n < self.dim:
                ram = init(self.dim)#初始化的范围
                relationVector.append(ram)
                n += 1
            relationVector = norm(relationVector)#归一化
            FBrelationVectorList[relation] = relationVector
        print("FBrelationVectorList,Number is %d"%len(FBrelationVectorList))
        self.FBentityList = FBentityVectorList
        self.FBrelationList = FBrelationVectorList
    def transE(self, cI = 20):
        print("Begian Train")
        for cycleIndex in range(cI):  #随机梯度下降
            S_DBbatch = self.getSample(100,"DB") #SGD的DBBatch
            S_FBbatch=self.getSample(100,"FB")#SGD的FBBatch
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
            print("%d"%cycleIndex)
            print(self.loss)
                #self.writeRelationVector("FB_relationVector.txt","FB")
                #self.writeEntilyVector("FB_entityVector.txt")
            self.loss = 0

    def getSample(self, size,index):
        if index=="DB":
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
                if index=="DB":
                    entityTemp = sample(self.DBentityList.keys(), 1)[0]
                else:
                    entityTemp = sample(self.FBentityList.keys(), 1)[0]
                if entityTemp != triplet[0]:
                    break
            corruptedTriplet = (entityTemp, triplet[1], triplet[2])
        else:#大于等于0，打坏三元组的第二项
            while True:
                if index=="DB":
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
            FBrelationVector = CP_FBRelationList[Corrupted_FBTriplet[0][2]]
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
            eg_FB=self.margin+distFB-dist_FBCorrupt
            for Corrupted_DBTriplet in T_DBbatch:
                head_DBEntityVector = CP_DBEntityList[Corrupted_DBTriplet[0][0]]#tripletWithCorruptedTriplet是原三元组和打碎的三元组的元组tuple
                tail_DBEntityVector = CP_DBEntityList[Corrupted_DBTriplet[0][1]]
                DBrelationVector = CP_DBRelationList[Corrupted_DBTriplet[0][2]]
                head_DBCorruptedTriplet = CP_DBEntityList[Corrupted_DBTriplet[1][0]]
                tail_DBCorruptedTriplet = CP_DBEntityList[Corrupted_DBTriplet[1][1]]
                head_DBBefore = self.DBentityList[Corrupted_DBTriplet[0][0]]#tripletWithCorruptedTriplet是原三元组和打碎的三元组的元组tuple
                tail_DBBefore= self.DBentityList[Corrupted_DBTriplet[0][1]]
                relation_DBBefore= self.DBrelationList[Corrupted_DBTriplet[0][2]]
                head_DBCorruptedBefore= self.DBentityList[Corrupted_DBTriplet[1][0]]
                tail_DBCorruptedBefore = self.DBentityList[Corrupted_DBTriplet[1][1]]
                if self.L1:
                    distDB = distanceL1(head_DBBefore, tail_DBBefore, relation_DBBefore)
                    dist_DBCorrupt= distanceL1(head_DBCorruptedBefore, tail_DBCorruptedBefore, relation_DBBefore)
                else:
                    distDB = distanceL2(head_DBBefore, tail_DBBefore, relation_DBBefore)
                    dist_DBCorrupt = distanceL2(head_DBCorruptedBefore, tail_DBCorruptedBefore ,  relation_DBBefore)
                try:
                    head_sameAsEntity=self.SameAs[Corrupted_FBTriplet[0][0]]
                    head_SameAsEntityVector = CP_DBEntityList[head_sameAsEntity]#tripletWithCorruptedTriplet是原三元组和打碎的三元组的元组tuple
                    head_SameAsBefore=self.DBentityList[head_sameAsEntity]
                    if head_sameAsEntity==Corrupted_DBTriplet[0][0]:
                        index_head=0
                    else:
                        index_head=1
                except Exception as e:
                    index_head=3
                try:
                    tail_sameAsEntity=self.SameAs[Corrupted_FBTriplet[0][1]]
                    tail_SameAsEntityVector = CP_DBEntityList[tail_sameAsEntity]#tripletWithCorruptedTriplet是原三元组和打碎的三元组的元组tuple
                    tail_SameAsBefore=self.DBentityList[tail_sameAsEntity]
                    if tail_sameAsEntity==Corrupted_DBTriplet[0][1]:
                        index_tail=0
                    else:
                        index_tail=1
                except Exception as e:
                    index_tail=3
                if self.L1:
                    if index_head!=3:
                        dist_HeadSameAs = distanceL1SameAs(head_FBBefore,head_SameAsBefore)
                    dist_HeadMapping=distanceL1SameAs(head_FBBefore,head_DBBefore)
                    if index_tail!=3:
                        dist_tailSameAs = distanceL1SameAs(tail_FBBefore,tail_SameAsBefore)
                    dist_tailMapping=distanceL1SameAs(tail_FBBefore,tail_DBBefore)
                    dist_relationMapping=distanceL1SameAs(relation_FBBefore,relation_DBBefore)
                else:
                    if index_head!=3:
                        dist_HeadSameAs = distanceL2SameAs(head_FBBefore,head_SameAsBefore)
                    dist_HeadMapping=distanceL2SameAs(head_FBBefore,head_DBBefore)
                    if index_tail!=3:
                        dist_tailSameAs = distanceL2SameAs(tail_FBBefore,tail_SameAsBefore)
                    dist_tailMapping=distanceL2SameAs(tail_FBBefore,tail_DBBefore)
                    dist_relationMapping=distanceL2SameAs(relation_FBBefore,relation_DBBefore)
                eg_DB = self.margin + distDB - dist_DBCorrupt
                if index_head==1:
                    eg_HeadSameAs=self.margin+dist_HeadSameAs-dist_HeadMapping
                elif index_head==0:
                    eg_HeadSameAs=dist_HeadMapping
                else:
                    eg_HeadSameAs=0
                if index_tail==1:
                    eg_tailSameAs=self.margin+dist_tailSameAs-dist_tailMapping
                elif index_tail==0:
                    eg_tailSameAs=dist_tailMapping
                else:
                    eg_tailSameAs=0
                if index_head==0 and index_tail==0:
                    eg_relation=dist_relationMapping
                else:
                    eg_relation=0
                eg=eg_FB+eg_DB+self.weight*(eg_HeadSameAs+eg_tailSameAs+eg_relation)
                if eg > 0: #[function]+ 是一个取正值的函数
                    self.loss += eg
                    temp_FBPositive = 2 * (tail_FBBefore - head_FBBefore - relation_FBBefore)
                    temp_FBNegtative = 2 * (tail_FBCorruptedBefore-head_FBCorruptedBefore-relation_FBBefore)
                    temp_DBPositive = 2 * (tail_DBBefore - head_DBBefore - relation_DBBefore)
                    temp_DBNegtative = 2 * (tail_DBCorruptedBefore-head_DBCorruptedBefore-relation_DBBefore)
                    if index_head!=3:
                        tem_HeadSameAs=2 * (head_SameAsBefore-head_FBBefore)
                    tem_HeadMapping=2 * (head_DBBefore-head_FBBefore)
                    if index_tail!=3:
                        tem_tailSameAs=2 * (tail_SameAsBefore-tail_FBBefore)
                    tem_tailMapping=2 * (tail_DBBefore-tail_FBBefore)
                    tem_relaion=2 * (relation_DBBefore-relation_FBBefore)
                    if self.L1:
                        temp_FBPositive = array([1 if index>0 else -1 for index in temp_FBPositive])
                        temp_FBNegtative = array([1 if index>0 else -1 for index in temp_FBNegtative])
                        temp_DBPositive = array([1 if index>0 else -1 for index in temp_DBPositive])
                        temp_DBNegtative = array([1 if index>0 else -1 for index in temp_DBNegtative])
                        if index_head!=3:
                            tem_HeadSameAs = array([1 if index>0 else -1 for index in tem_HeadSameAs])
                        tem_HeadMapping = array([1 if index>0 else -1 for index in tem_HeadMapping])
                        if index_tail!=3:
                            tem_tailSameAs = array([1 if index>0 else -1 for index in tem_tailSameAs])
                        tem_tailMapping = array([1 if index>0 else -1 for index in tem_tailMapping])
                        tem_relaion = array([1 if index>0 else -1 for index in tem_relaion])
                    if index_head==1:
                        head_FBEntityVector = head_FBEntityVector + self.learingRate*(temp_FBPositive+tem_HeadSameAs-tem_HeadMapping)
                        head_SameAsEntityVector=head_SameAsEntityVector-self.learingRate*(tem_HeadSameAs)
                        head_DBEntityVector=head_DBEntityVector+self.learingRate*(temp_DBPositive+tem_HeadMapping)
                    elif index_head==0:
                        head_FBEntityVector = head_FBEntityVector + self.learingRate*(temp_FBPositive+tem_HeadMapping)
                        head_DBEntityVector=head_DBEntityVector+self.learingRate*(temp_DBPositive-tem_HeadMapping)
                    else:
                        head_FBEntityVector=head_FBEntityVector+self.learingRate*temp_FBPositive
                        head_DBEntityVector=head_DBEntityVector+self.learingRate*temp_DBPositive
                    if index_tail==1:
                        tail_FBEntityVector=tail_FBEntityVector+self.learingRate*(-temp_FBPositive+tem_tailSameAs-tem_tailMapping)
                        tail_SameAsEntityVector=tail_SameAsEntityVector-self.learingRate*(tem_tailSameAs)
                        tail_DBEntityVector=tail_DBEntityVector+self.learingRate*(-temp_DBPositive+tem_tailMapping)
                    elif index_tail==0:
                        tail_FBEntityVector=tail_FBEntityVector+self.learingRate*(-temp_FBPositive+tem_tailMapping)
                        tail_DBEntityVector=tail_DBEntityVector+self.learingRate*(-temp_DBPositive-tem_tailMapping)
                    else:
                        tail_DBEntityVector-=self.learingRate*temp_DBPositive
                        tail_FBEntityVector-=self.learingRate*temp_FBNegtative
                    if index_tail==0 and index_head==0:
                        FBrelationVector=FBrelationVector+self.learingRate*(temp_FBPositive-temp_FBNegtative+tem_relaion)
                        DBrelationVector=DBrelationVector+self.learingRate*(temp_DBPositive-temp_DBNegtative-tem_relaion)
                    else:
                        FBrelationVector=FBrelationVector+self.learingRate*(temp_FBPositive-temp_FBNegtative)
                        DBrelationVector=DBrelationVector+self.learingRate*(temp_DBPositive-temp_DBNegtative)
                    head_FBCorruptedTriplet=head_FBCorruptedTriplet-self.learingRate*temp_FBNegtative
                    tail_FBCorruptedTriplet=tail_FBCorruptedTriplet+self.learingRate*temp_FBNegtative
                    head_DBCorruptedTriplet=head_DBCorruptedTriplet-self.learingRate*temp_DBNegtative
                    tail_DBCorruptedTriplet=tail_DBCorruptedTriplet+self.learingRate*temp_DBNegtative
                    #只归一化这几个刚更新的向量
                    CP_FBEntityList[Corrupted_FBTriplet[0][0]] = norm(head_FBEntityVector)
                    CP_FBEntityList[Corrupted_FBTriplet[0][1]] = norm(tail_FBEntityVector)
                    CP_FBRelationList[Corrupted_FBTriplet[0][2]] = norm(FBrelationVector)
                    CP_FBEntityList[Corrupted_FBTriplet[1][0]] = norm(head_FBCorruptedTriplet)
                    CP_FBEntityList[Corrupted_FBTriplet[1][1]] = norm(tail_FBCorruptedTriplet)
                    CP_DBEntityList[Corrupted_DBTriplet[0][0]] = norm(head_DBEntityVector)
                    CP_DBEntityList[Corrupted_DBTriplet[0][1]] = norm(tail_DBEntityVector)
                    CP_DBRelationList[Corrupted_DBTriplet[0][2]] = norm(DBrelationVector)
                    CP_DBEntityList[Corrupted_DBTriplet[1][0]] = norm(head_DBCorruptedTriplet)
                    CP_DBEntityList[Corrupted_DBTriplet[1][1]] = norm(tail_DBCorruptedTriplet)
                    if index_tail!=3:
                        CP_DBEntityList[tail_sameAsEntity]=norm(tail_SameAsEntityVector)
                    if index_head!=3:
                        CP_DBEntityList[head_sameAsEntity]=norm(head_SameAsEntityVector)
        self.FBentityList = CP_FBEntityList
        self.FBrelationList = CP_FBRelationList
        self.DBentityList=CP_DBEntityList
        self.DBrelationList=CP_DBRelationList

    def writeEntilyVector(self, dir, index):
        print("")
        entityVectorFile = open(dir, 'w')
        if index=="FB":
            for entity in self.FBentityList.keys():
                entityVectorFile.write(entity+"\t")
                entityVectorFile.write(str(self.FBentityList[entity].tolist()))
                entityVectorFile.write("\n")
            entityVectorFile.close()
        else:
            for entity in self.DBentityList.keys():
                entityVectorFile.write(entity+"\t")
                entityVectorFile.write(str(self.DBentityList[entity].tolist()))
                entityVectorFile.write("\n")
            entityVectorFile.close()
    def writeRelationVector(self, dir,index):
        print("")
        relationVectorFile = open(dir, 'w')
        if index=="FB":
            for relation in self.FBrelationList.keys():
                relationVectorFile.write(relation + "\t")
                relationVectorFile.write(str(self.FBrelationList[relation].tolist()))
                relationVectorFile.write("\n")
            relationVectorFile.close()
        else:
            for relation in self.DBrelationList.keys():
                relationVectorFile.write(relation + "\t")
                relationVectorFile.write(str(self.DBrelationList[relation].tolist()))
                relationVectorFile.write("\n")
            relationVectorFile.close()

def init(dim):
    return uniform(-6/(dim**0.5), 6/(dim**0.5))

def distanceL1(h, t ,r):
    s = h + r - t
    sum = fabs(s).sum()
    return sum
def distanceL1SameAs(h, t):
    s = h - t
    sum = fabs(s).sum()
    return sum

def distanceL2(h, t, r):
    s = h + r - t
    sum = (s*s).sum()
    return sum
def distanceL2SameAs(h, t):
    s = h - t
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

def openDetailsAndId(dir,sp="\t"):
    idNum = 0
    list = []
    with open(dir) as file:
        lines = file.readlines()
        for line in lines:
            DetailsAndId = line.strip().split(sp)
            list.append(DetailsAndId[0])
            idNum += 1
    return idNum, list
def openSameAs(dir,sp="\t"):
    idNum = 0
    list = {}
    with open(dir) as file:
        lines = file.readlines()
        for line in lines:
            DetailsAndId = line.strip().split(sp)
            list[DetailsAndId[1]]=DetailsAndId[0]
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
    dirFBEntity = "/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/entity_FB2id.txt"
    FBentityIdNum, entityFBList = openDetailsAndId(dirFBEntity)
    dirDBEntity = "/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/entity_DB2id.txt"
    DBentityIdNum, entityDBList = openDetailsAndId(dirDBEntity)
    dirFBRelation = "/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/FB_relation2id.txt"
    FBrelationIdNum, relationFBList = openDetailsAndId(dirFBRelation)
    dirDBRelation = "/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/DB_relation2id.txt"
    DBrelationIdNum, relationDBList = openDetailsAndId(dirDBRelation)
    dirFBTrain = "/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/train_FB.txt"
    FBtripleNum, tripleFBList = openTrain(dirFBTrain)
    dirDBTrain = "/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/train_DB.txt"
    DBtripleNum, tripleDBList = openTrain(dirDBTrain)
    dirsameAs="/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/test_Entity.txt"
    SameAsNum, SameAsList=openSameAs(dirsameAs)
    print("Open TransE")
    transE = TransE(entityDBList,relationDBList,tripleDBList,entityFBList,relationFBList,tripleFBList,SameAsList, margin=2, dim = 50, L1 = True, weight=5)
    print("TranE")
    transE.initialize()
    transE.transE(5000)
    transE.writeRelationVector("/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/FBrelationVector.txt","FB")
    transE.writeRelationVector("/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/DBrelationVector.txt","DB")
    transE.writeEntilyVector("/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/FBentityVector.txt","FB")
    transE.writeEntilyVector("/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/DBentityVector.txt","DB")
    print("Begain")
    dirEntityTest =  "/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/test_Entity.txt"
    EntityTest = MGTest.openD(dirEntityTest)
    print("Read Entity")
    dirRelationTest = "/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/test_Relation.txt"
    RelationTest = MGTest.openD(dirRelationTest)
    print("Read Relation")
    dirFBEntityVector = "/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/FBentityVector.txt"
    FBentityVectorList, FBentityList = MGTest.loadData(dirFBEntityVector)
    print("Read FBEntitVector")
    dirFBRelationVector = "/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/FBrelationVector.txt"
    FBrelationVectorList, FBrelationList = MGTest.loadData(dirFBRelationVector)
    dirDBEntityVector = "/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/DBentityVector.txt"
    DBentityVectorList, DBentityList = MGTest.loadData(dirDBEntityVector)
    print("Read FBEntitVector")
    dirDBRelationVector = "/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/DBrelationVector.txt"
    DBrelationVectorList, DBrelationList = MGTest.loadData(dirDBRelationVector)
    print("Read RelationVector")
    testHeadRaw = MGTest.Test(FBentityList, FBentityVectorList, FBrelationList, FBrelationVectorList, DBentityList, DBentityVectorList, DBrelationList, DBrelationVectorList, EntityTest, RelationTest)
    testHeadRaw.getRank()
    print("MeanRank of HeadRaw is %f"%(testHeadRaw.getMeanRank()))
    testHeadRaw.writeRank("/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/" + "MGtestHeadRaw" + ".txt")
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

    testHeadRaw.getRelationRank()
    print("MeanRank of Relation is %f"%(testHeadRaw.getMeanRank()))
    testHeadRaw.writeRank("/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/" + "testRelationRaw" + ".txt")
    testTailRaw = test.Test(entityList, entityVectorList, relationList, relationVectorList, EntityTest, RelationTest, label = "tail")
    testTailRaw.getRank()
    print("MeanRank of HeadRaw is %f"%(testHeadRaw.getMeanRank()))
    print("MeanRank of TailRaw is %f"%(testTailRaw.getMeanRank()))
    testTailRaw.writeRank("/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/" + "testTailRaw" + ".txt")
    print("Done")
    """
