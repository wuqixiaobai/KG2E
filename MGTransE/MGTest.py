#-*- coding:utf-8 –*-
from numpy import *
import operator

class Test:
    def __init__(self, FBentityList, FBentityVectorList, FBrelationList, FBrelationVectorList, DBentityList, DBentityVectorList, DBrelationList, DBrelationVectorList,EntitySameAsTest, SchemaTest, label = "head"):
        self.FBentityList = {} #key is entity, value is the Vector
        self.FBrelationList = {}
        self.DBentityList = {} #key is entity, value is the Vector
        self.DBrelationList = {}
        for name, vec in zip(FBentityList, FBentityVectorList):
            self.FBentityList[name] = vec
        for name, vec in zip(FBrelationList, FBrelationVectorList):
            self.FBrelationList[name] = vec #key is relation
        for name, vec in zip(DBentityList, DBentityVectorList):
            self.DBentityList[name] = vec
        for name, vec in zip(DBrelationList, DBrelationVectorList):
            self.DBrelationList[name] = vec #key is relation
        self.EntitySameAsTest = EntitySameAsTest #EntitySameAsTest[0] and EntitySameAsTest[1]
        self.SchemaTest = SchemaTest  #SchemaTest[0] and SchemaTest[1]
        self.rank = []
        self.label = label
    def writeRank(self, dir):
        print("写入")
        file = open(dir, 'w')
        for r in self.rank:
            file.write(str(r[0]) + "\t")
            file.write(str(r[1]) + "\t")
            file.write(str(r[2]) + "\t")
            file.write(str(r[3]) + "\n")
        file.close()

    def getRank(self):
        print("Test")
        TopIndex=0.0
        ToponeIndex=0.0
        cou = 0
        for sameAs in self.EntitySameAsTest:
            rankList = {}
            if self.label == "head": # Replace Head
                for entityTemp in self.DBentityList.keys():
                    corruptedTriplet = (entityTemp, sameAs[1])
                    rankList[entityTemp] = distance(self.DBentityList[entityTemp], self.FBentityList[sameAs[1]])
            else:
                for entityTemp in self.FBentityList.keys():
                    corruptedTriplet = (sameAs[0], entityTemp)
                    rankList[entityTemp] = distance(self.DBentityList[sameAs[0]], self.FBentityList[entityTemp])
            nameRank = sorted(rankList.items(), key = operator.itemgetter(1))
            if self.label == 'head':
                numTri = 0
            else:
                numTri = 1
            x = 1
            for i in nameRank:
                if i[0] == sameAs[numTri]:
                    break
                x += 1
            if x<=10:
                TopIndex+=1
            if x==1:
                ToponeIndex+=1
            self.rank.append((sameAs, sameAs[numTri], nameRank[0][0], x))
            cou += 1
            if cou % 10000 == 0:
                print(cou)
        return TopIndex /len(self.EntitySameAsTest),ToponeIndex /len(self.EntitySameAsTest)
    def getRelationRank(self):
        cou = 0
        TopIndex=0.0
        ToponeIndex=0.0
        self.rank = []
        for Schema in self.SchemaTest:
            rankList = {}
            if self.label == "head": # Replace Head
                for entityTemp in self.FBrelationList.keys():
                    corruptedTriplet = (entityTemp, Schema[1])
                    rankList[entityTemp] = distance(self.FBrelationList[entityTemp],self.DBrelationList[Schema[1]])
            else:
                for entityTemp in self.DBrelationList.keys():
                    corruptedTriplet = (Schema[0], entityTemp)
                    rankList[entityTemp] = distance(self.DBrelationList[sameAs[0]],self.FBrelationList[entityTemp])
            nameRank = sorted(rankList.items(), key = operator.itemgetter(1))
            if self.label == 'head':
                numTri = 0
            else:
                numTri = 1
            x = 1
            for i in nameRank:
                if i[0] == Schema[numTri]:
                    break
                x += 1
            if x<=10:
                TopIndex+=1
            if x==1:
                ToponeIndex+=1
            self.rank.append((Schema, Schema[numTri], nameRank[0][0], x))
            cou += 1
            if cou % 10000 == 0:
                print(cou)
        return TopIndex /len(self.SchemaTest),ToponeIndex /len(self.SchemaTest)
    def getMeanRank(self):
        num = 0
        for r in self.rank:
            num += r[3]
        return num/len(self.rank)


def distance(h, t):
    h = array(h)
    t = array(t)
    s = h - t

    return linalg.norm(s)

def openD(dir, sp="\t"):
    #triple = (entity, entity) or (relation,relation)
    list = []
    with open(dir) as file:
        lines = file.readlines()
        for line in lines:
            triple = line.strip().split(sp)
            list.append([triple[0],triple[1]])
    return list

def loadData(str):
    fr = open(str)
    sArr = [line.strip().split("\t") for line in fr.readlines()]
    datArr = [[float(s) for s in line[1][1:-1].split(", ")] for line in sArr]
    nameArr = [line[0] for line in sArr]
    return datArr, nameArr

if __name__ == '__main__':
    print("Begain")
    dirEntityTest =  "/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/test_Entity.txt"
    EntityTest = openD(dirEntityTest)
    print("Read Entity")
    dirRelationTest = "/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/test_Relation.txt"
    RelationTest = openD(dirRelationTest)
    print("Read Relation")
    dirFBEntityVector = "/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/FBentityVector.txt"
    FBentityVectorList, FBentityList = loadData(dirFBEntityVector)
    print("Read FBEntitVector")
    dirFBRelationVector = "/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/FBrelationVector.txt"
    FBrelationVectorList, FBrelationList = loadData(dirFBRelationVector)
    dirDBEntityVector = "/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/DBentityVector.txt"
    DBentityVectorList, DBentityList = loadData(dirDBEntityVector)
    print("Read FBEntitVector")
    dirDBRelationVector = "/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/DBrelationVector.txt"
    DBrelationVectorList, DBrelationList = loadData(dirDBRelationVector)
    print("Read RelationVector")
    testHeadRaw = Test(FBentityList, FBentityVectorList, FBrelationList, FBrelationVectorList, DBentityList, DBentityVectorList, DBrelationList, DBrelationVectorList, EntityTest, RelationTest)
    testHeadRaw.getRank()
    print("MeanRank of HeadRaw is %f"%(testHeadRaw.getMeanRank()))
    testHeadRaw.writeRank("/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/" + "MGtestHeadRaw" + ".txt")
    """
    testHeadRaw.getRelationRank()
    print("MeanRank of Relation is %f"%(testHeadRaw.getMeanRank()))
    testHeadRaw.writeRank("/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/" + "testRelationRaw" + ".txt")
    """
    testTailRaw = Test(entityList, entityVectorList, relationList, relationVectorList, EntityTest, RelationTest, label = "tail")
    testTailRaw.getRank()
    print("MeanRank of HeadRaw is %f"%(testHeadRaw.getMeanRank()))
    print("MeanRank of TailRaw is %f"%(testTailRaw.getMeanRank()))
    testTailRaw.writeRank("/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/" + "MGtestTailRaw" + ".txt")
    print("Done")
