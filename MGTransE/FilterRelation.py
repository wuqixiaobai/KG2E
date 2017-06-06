class Filter(object):
    def Filter_Relaton(self, dir):
        result = {}  # key is Relation, value is None
        sp = "\t"
        index = 0
        with open(dir) as file:
            line = file.readline()
            while line:
                index += 1
                StringEntity = line.strip().split(sp)  # line is a triple 
                Entity_DB1 = StringEntity[0]
                Entity_DB2 = StringEntity[1]
                Entity_rl3 = StringEntity[2][27:]
                keyEntity = Entity_DB1 + "\t" + Entity_DB2
                if keyEntity not in result.keys():
                    result[keyEntity] = [] + [Entity_rl3]
                else:
                    value = result.get(keyEntity)
                    if Entity_rl3 not in value:
                        result[keyEntity] = result[keyEntity] + [Entity_rl3]
                line = file.readline()
        return result

    def Filter_DuRelaton(self, dir):
        result = {}  # key is Relation, value is None
        sp = "\t"
        index = 0
        with open(dir) as file:
            line = file.readline()
            while line:
                index += 1
                StringEntity = line.strip().split(sp)  # line is a triple 
                Entity_DB1 = StringEntity[0]
                Entity_DB2 = StringEntity[1]
                if Entity_DB2 != "-1":
                    result[Entity_DB1] = Entity_DB2[27:]
                line = file.readline()
        return result


if __name__ == '__main__':
    DBtraindir = "/Users/wenqiangliu/Documents/KG2E/data/DB_Fb30k/DBRelation.txt"
    DBtrain = Filter().Filter_Relaton(DBtraindir)
    Indexnumber = {}
    for key, value in DBtrain.items():
        number = len(value)
        Indexnumber[key] = number
    Duplit = []
    for key, value in Indexnumber.items():
        if value >= 2:
            Duplit.append(key)
    print(len(Duplit))
    for entities in Duplit:
        Relation_list = DBtrain[entities]
        DBtrain[entities] = [Relation_list[0]]
    SameAsFile = open(
        "/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/train_DB.txt", 'w')
    RelationId = {}
    for key, value in DBtrain.items():
        SameAsFile.write(key + "\t" + "".join(value) + "\n")
        if "".join(value) not in RelationId.keys():
            RelationId["".join(value)] = ''
    DBrelationdir = "/Users/wenqiangliu/Documents/KG2E/data/DB_Fb30k/RelationMapping.txt"
    RelationMapping = Filter().Filter_DuRelaton(DBrelationdir)
    RelationFile = open(
        "/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/test_Relation.txt",
        'w')
    for key, value in RelationMapping.items():
        RelationFile.write(key + "\t" + value + "\n")
    RelationIDFile = open("/Users/wenqiangliu/Documents/KG2E/data/DB_FB30k/DB_Relation2id.txt",'w')
    id = 1
    for key, value in RelationId.items():
        RelationIDFile.write(("%s\t%d") % (key, id)+"\n")
        id += 1
