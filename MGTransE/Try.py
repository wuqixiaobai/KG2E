from numpy import *
dir="/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/train.txt"
idNum = 0
sp="\t"
list1 = []
with open(dir) as file:
  lines = file.readline()
  while lines:
    DetailsAndId = lines.strip().split(sp)
    print(DetailsAndId[2])
    lines = file.readline()
"""
dirt="/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/SameasRealtion.txt"
relationVectorFile = open(dirt, 'w')
for relation in list1:
  relationVectorFile.write(relation+"\t"+"/sameAs"+"\n")
"""
