import string
valueDict={}
id=-1
# newfile holds the yml file with only id and value in continuous lines
with open("newfile", "r") as input:
    for line in input:
        if "id:" in line:
            id=int(line.split()[1].translate(str.maketrans('', '', string.punctuation)))
        if "value" in line:
            value = line.split()[1]
            valueDict[id]=value
print(valueDict)
# valueDict holds the dictionary with key as id and value as entailment value

