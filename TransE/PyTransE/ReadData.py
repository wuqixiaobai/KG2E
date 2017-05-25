#-*- coding:utf-8 –*-
from random import uniform, sample
from numpy import *
from copy import deepcopy
import ConnectEndPoint
from SPARQLWrapper import SPARQLWrapper, JSON
FBdir = "/Users/wenqiangliu/Documents/KG2E/data/FB15k/entity2id.txt"
sp = "\t"
idNum = 0
FBdic = {}  # freebase Entity,key is entity; value=-1
with open(FBdir) as file:
    print("Begain Reading Freebase File")
    lines = file.readlines()
    for line in lines:
        DetailsAndId = line.strip().split(sp)
        FBdic[DetailsAndId[0][1:].replace("/", ".")] = -1
        idNum += 1
file.close()
print("The Freebase Fils is Done")
DB_FB_dir = "/Users/wenqiangliu/Desktop/freebase_links_en.nt"  # 读取DBpedia Links to freebase
splinks = " "
DBdic = {}  # Dbpedia dic, key is entity and value is freebase entity
idNum = 0
with open(DB_FB_dir) as file:
    print("Begain Extract DBpedia Entity")
    lines = file.readlines()
    for line in lines:
        DetailsAndId = line.strip().split(splinks)
        db = DetailsAndId[0][1:-1]
        fb = DetailsAndId[2][28:-1]
        if fb in FBdic.keys():
            DBdic[db] = fb
        idNum += 1
print("The DBpedia Entity is ready, the total number of entity is %d" %(len(DBdic)))
endpoint = "http://dbpedia.org/sparql/"
error = 0
print("Remove Duplicates")
CopyDBdic = deepcopy(DBdic)
index=0
for dic in DBdic.keys():
    sparqlString = "select ?p ?o where {<" + dic + "> ?p ?o}"
    index+=1
    if index % 100 ==0:
        print("Processing the %d"%(index))
    biordfsparql = ConnectEndPoint.ConnectEnd(endpoint, sparqlString)
    results = biordfsparql.Connect()
    for result in results["results"]["bindings"]:
        if result["p"]["value"] == "http://dbpedia.org/ontology/wikiPageRedirects":
            if result["o"]["value"] in DBdic.keys():
                CopyDBdic.pop(dic)
            else:
                error += 1
DBdic = CopyDBdic
print("The length of DBpedia dic is  %d" % (len(DBdic)))
print("Remove Duplicates is Done, the error is %d" % (error))
print("Writing Entity")
entityFile = open("/Users/wenqiangliu/Documents/KGEmbedding/data/FB15k/entity_DBpedi2id.txt",'w')
SameAsFile = open("/Users/wenqiangliu/Documents/KGEmbedding/data/FB15k/DB_FB.txt", 'w')
entityId = 1
for entity in DBdic.keys():
    entityFile.write(entity + "\t" + entityId)
    SameAsFile.write(entity + "\t" + DBdic[entity])
    entityId += 1
print("All are Done!")
