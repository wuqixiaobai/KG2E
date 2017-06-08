#-*- coding:utf-8 –*-
from numpy import *
import operator

class Test:
    def __init__(self, entityList, entityVectorList, relationList, relationVectorList, EntitySameAsTest, SchemaTest, label = "head"):
        self.entityList = {} #key is entity, value is the Vector
        self.relationList = {}
        for name, vec in zip(entityList, entityVectorList):
            self.entityList[name] = vec
        for name, vec in zip(relationList, relationVectorList):
            self.relationList[name] = vec #key is relation
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
        print("开始测试")
        cou = 0
        for sameAs in self.EntitySameAsTest:
            rankList = {}
            if self.label == "head": # Replace Head
                for entityTemp in self.entityList.keys():
                    corruptedTriplet = (entityTemp, sameAs[1])
                    rankList[entityTemp] = distance(self.entityList[entityTemp], self.entityList[sameAs[1]])
            else:
                for entityTemp in self.entityList.keys():
                    corruptedTriplet = (sameAs[0], entityTemp)
                    rankList[entityTemp] = distance(self.entityList[sameAs[0]], self.entityList[entityTemp])
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
            self.rank.append((sameAs, sameAs[numTri], nameRank[0][0], x))
            cou += 1
            if cou % 10000 == 0:
                print(cou)

    def getRelationRank(self):
        cou = 0
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
            self.rank.append((Schema, Schema[numTri], nameRank[0][0], x))
            cou += 1
            if cou % 10000 == 0:
                print(cou)

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
    dirEntityVector = "/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/entityVector.txt"
    entityVectorList, entityList = loadData(dirEntityVector)
    print("Read EntitVector")
    dirRelationVector = "/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/relationVector.txt"
    relationVectorList, relationList = loadData(dirRelationVector)
    print("Read RelationVector")
    testHeadRaw = Test(entityList, entityVectorList, relationList, relationVectorList, EntityTest, RelationTest)
    testHeadRaw.getRank()
    print("MeanRank of HeadRaw is %f"%(testHeadRaw.getMeanRank()))
    testHeadRaw.writeRank("/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/" + "testHeadRaw" + ".txt")
    """
    testHeadRaw.getRelationRank()
    print("MeanRank of Relation is %f"%(testHeadRaw.getMeanRank()))
    testHeadRaw.writeRank("/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/" + "testRelationRaw" + ".txt")
    """
    testTailRaw = Test(entityList, entityVectorList, relationList, relationVectorList, EntityTest, RelationTest, label = "tail")
    testTailRaw.getRank()
    print("MeanRank of HeadRaw is %f"%(testHeadRaw.getMeanRank()))
    print("MeanRank of TailRaw is %f"%(testTailRaw.getMeanRank()))
    testTailRaw.writeRank("/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/" + "testTailRaw" + ".txt")
    print("Done")
