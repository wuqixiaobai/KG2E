from numpy import *
dir="/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/testRelationRaw.txt"
sp="\t"
idNum=0.0
TopTen=0.0
with open(dir) as file:
  lines = file.readline()
  while lines:
    DetailsAndId = lines.strip().split(sp)
    idNum += 1
    if int(DetailsAndId[3])<=100:
      TopTen+=1
    lines = file.readline()
print(TopTen/idNum)
