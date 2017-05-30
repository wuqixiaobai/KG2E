#-*- coding:utf-8 –*-
from copy import deepcopy
from collections import Counter
from SPARQLWrapper import SPARQLWrapper, JSON
def Extract_Relation(dirTrain= "data/DB_FB30k/FB_relation2id.txt"):
  result = {} # key is Relation, value is None
  sp = "\t"
  with open(dirTrain) as file:
    line=file.readline()
    while line:
      StringEntity = line.strip().split(sp) # line is a triple
      Entity_FB1=StringEntity[0]
      result[Entity_FB1]=-1
      line=file.readline()
  return result
def Extract_FB(dirTrain= "data/FB15k/train.txt"):
  result = {} # key is Relation, value is a list which has a special realtion between entity
  sp = "\t"
  with open(dirTrain) as file:
    line=file.readline()
    while line:
      StringEntity = line.strip().split(sp) # line is a triple
      Relation=StringEntity[2]
      Entity_FB1=StringEntity[0]
      Entity_FB2=StringEntity[1]
      tempList=[Entity_FB1+"\t"+Entity_FB2]
      if Relation in result.keys():
        result[Relation]=result[Relation]+tempList
      else:
        result[Relation]=tempList
      line=file.readline()
  return result
def MacthDB(dirTrain):
  result={} # key is the FB, value is DB
  sp="\t"
  with open(dirTrain) as file:
    line=file.readline()
    while line:
      StringEntity=line.strip().split(sp) # line is a triple
      Entity_DB=StringEntity[0]
      Entity_FB=StringEntity[1]
      result[Entity_FB]=Entity_DB
      line=file.readline()
  return result
def SparqlQuery(endpoint, spaqlString):
  try:
    sparql = SPARQLWrapper(endpoint)  # The endpoint
    sparql.setQuery(sparqlString)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    queryresult=[]
    for result in results["results"]["bindings"]:
      queryresult.append(result["p"]["value"])
  except:
    print(sparqlString)
  return queryresult
if __name__ == '__main__':
  Relation = Extract_Relation()
  print("Extract Relation is Done")
  FB_FB=Extract_FB() # Extract FB-FB From Train text
  print("Extract FB is Done, the length is %d"%(len(FB_FB)))
  dirMathDB= "data/DB_FB30k/SameAsRelation.txt"
  FB_DB=MacthDB(dirMathDB)
  print("Extract FB_DB is Done")
  Copyrelation=deepcopy(Relation)
  index=1.0
  DBRelation=[]
  for keys in Relation.keys():
    listFB=FB_FB[keys]
    print("Has processing the %d(All is 1345) And the size of Relation is %d "%(index, len(listFB)))
    Relation_Result=[]
    for entity in listFB:
      if entity.split("\t")[0] in FB_DB.keys() and entity.split("\t")[1] in FB_DB.keys():
        DBEntity1 = FB_DB[entity.split("\t")[0]]
        DBEntity2 = FB_DB[entity.split("\t")[1]]
        sparqlString="select ?p where { <http://dbpedia.org/resource"+DBEntity1+"> ?p"+" <http://dbpedia.org/resource"+DBEntity2+"> }"
        #print(sparqlString)
        try:
          result=SparqlQuery("http://dbpedia.org/sparql/",sparqlString)
        except:
          continue
        if result!=[]:
          Relation_Result+=result
          for relation in result:
            DBRelation.append(DBEntity1+"\t"+DBEntity2+"\t"+result)
      else:
        continue
    if Relation_Result!=[]:
      NumberCounter=Counter(Relation_Result)
      Relation[keys]=NumberCounter.most_common(1)[0][0]
    else:
      Relation[keys]="-1"
    index+=1
  SameAsFile = open("data/DB_FB30k/RelationMapping.txt", 'w')
  DBRelationFile = open("data/DB_FB30k/DBRelation.txt", 'w')
  for entity in Relation.keys():
    SameAsFile.write(entity + "\t" + Relation[entity]+"\n")
  for relation in range(len(DBRelation)):
    DBRelationFile.write(DBRelation[relation]+"\n")
  print("All are Done!")
