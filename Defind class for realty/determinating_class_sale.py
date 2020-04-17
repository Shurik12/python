import os

def get_class_a():
    class_a = []
    file = os.path.join(os.path.dirname(__file__), "Class_A.tsv")
    with open(file, "r") as f_r:
        for line in f_r:
            line = line.strip('\n').split('\t')
            class_a.append(line)
    return class_a

def check_is_c(line):
    price = line[1]
    buildyear = line[7]
    floorscount = line[8]
    buildingclass = line[6]
    if "c" in buildingclass:
        return 1
    if floorscount.strip() != "None":
        if int(floorscount) <= 4:
            return 1
    if buildyear.strip() != "None":    
        if int(buildyear) > 1000 and int(buildyear) <= 2000:
            return 1
    return 0

def check_is_b(line):
    price = line[1].strip()
    buildyear = line[7].strip()
    floorscount = line[8].strip()
    buildingclass = line[6].strip()
    if "b" in buildingclass:
        return 1
    if floorscount.strip() != "None":
        if int(floorscount) <= 7:
            return 1
    if buildyear.strip() != "None":
        if int(buildyear) > 1000 and int(buildyear) <= 2010:
            return 1
    return 0

def get_class(line):
    class_a = get_class_a()
    if line[2:6] in class_a:
        return 'a'
    elif check_is_c(line):
        return 'c'
    elif check_is_b(line):
        return 'b'
    else:
        return 'None'