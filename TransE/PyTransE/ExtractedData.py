#-*- coding:utf-8 –*-
from copy import deepcopy
from SPARQLWrapper import SPARQLWrapper, JSON
FBdir = "/Users/wenqiangliu/Documents/KG2E/data/DB_FB/chongfu.txt"
sp = "\t"
idNum = 0
FBdic = {}  # freebase Entity,key is entity; value=-1
Chongfu = {}
with open(FBdir) as file:
    print("Begain Reading DB-To_FB File")
    lines = file.readline()
    while lines:
        DetailsAndId = lines.strip().split(sp)
        DBEntity = DetailsAndId[0]
        FreebaseEntity = DetailsAndId[1]
        Chongfu[DBEntity]=FreebaseEntity
        if FreebaseEntity in FBdic.keys():
            FBdic[FreebaseEntity]+=1
        else:
            FBdic[FreebaseEntity]=1
        lines = file.readline()
file.close()
index=1
Du_entity=[]#list of freebase entity whose number more than2
MoreDic={}
for ky,va in FBdic.items():
    if va>=2:
        Du_entity.append(ky)
for ky, va in Chongfu.items():
    if va in Du_entity:
        MoreDic[ky]=va
"""
DB_FB_dir = "/Users/wenqiangliu/Desktop/freebase_links_en.nt"  # 读取DBpedia Links to freebase
splinks = " "
SameAs = {}  # Dbpedia dic, key is entity and value is freebase entity
idNum = 0
with open(DB_FB_dir) as file:
    print("Begain Extract DBpedia Entity")
    line = file.readline()
    while line:
        DetailsAndId = line.strip().split(splinks)
        db = DetailsAndId[0][1:-1]  #DBpedia
        fb = DetailsAndId[2][28:-1] #Freebase
        SameAs[db]=fb
        line = file.readline()
CopyDBdic = deepcopy(FBdic)
for db in FBdic.keys():
    if db not in SameAs.keys():
        CopyDBdic.pop(db)
print("Begain SPAQL")
"""
CopyChongfu = deepcopy(Chongfu)
endpoint = "http://dbpedia.org/sparql/"
index1 = 0
sparql = SPARQLWrapper(endpoint)  # The endpoint
for entity in Du_entity:
    DBlist=[]
    index1+=1
    for ky, va in MoreDic.items():
        if va == entity:
            DBlist.append(ky)
    maxvalue =0
    maxindex=""
    for dic in DBlist:
        sparqlString = "select ?p ?o where { <"+ dic+"> ?p ?o}"
        index =0
        try:
            sparql.setQuery(sparqlString)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            queryresult=""
            for result in results["results"]["bindings"]:
                index+=1
        except:
            continue
        if index > maxvalue:
            maxvalue=index
            maxindex=dic
    for ky,va in CopyChongfu.items():
        if va==entity and ky!=maxindex:
            Chongfu.pop(ky)
    print("%d,%d"%(len(Du_entity)-index1,index))
print("writing")
SameAsFile = open("/Users/wenqiangliu/Documents/KG2E/data/DB_FB/chongfu_1.txt",'w')
entityId = 1
for entity in Chongfu.keys():
  StringDB_FB="%s\t%s"%(entity,Chongfu[entity])
  SameAsFile.write(StringDB_FB+"\n")
  entityId += 1
print("All are Done! %d"%(entityId))
"""
SameAsFile = open("/Users/wenqiangliu/Documents/KG2E/data/FB15k/DB_FB.txt",'w')
errorString =""
for entity in DBdic.keys():
  #StringDB="%s\t%d"%(CopyDBdic[entity],entityId)
  #entityFile.write(StringDB+"\n")
  try:
    StringDB_FB="%s\t%s"%(DBdic[entity],entity)
    SameAsFile.write(StringDB_FB+"\n")
  except:
    continue
print("All are Done!")
entityFile = open("/Users/wenqiangliu/Documents/KG2E/data/FB15k/entity_DBpedi2id.txt", 'w')
SameAsFile = open("/Users/wenqiangliu/Documents/KG2E/data/FB15k/FB_DB.txt",'w')
entityId = 1
for entity in CopyDBdic.keys():
  StringDB="%s\t%d"%(entity,entityId)
  entityFile.write(StringDB+"\n")
  StringDB_FB="%s\t%s"%(entity,CopyDBdic[entity])
  SameAsFile.write(StringDB_FB+"\n")
  entityId += 1
print("All are Done! %d"%(entityId))
SameAsFile = open("/Users/wenqiangliu/Documents/KG2E/data/DB_FB/chongfu.txt",'w')
entityId = 1
for entity in DBdic.keys():
  StringDB_FB="%s\t%s"%(entity,DBdic[entity])
  SameAsFile.write(StringDB_FB+"\n")
  entityId += 1
print("All are Done! %d"%(entityId))
"""
