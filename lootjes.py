import random
import json
import time

deelnemers = []
lootjesdict = {}
names = False
aantaldeelnemers = 0

def nameoverwritecheck(canidates, currentanwser):
        nameoverwrite = False
        for x in range(aantaldeelnemers):
            if canidates[x] == currentanwser:
                nameoverwrite = True
            else: 
                None
        if nameoverwrite == True:
            return nameoverwrite
        else:
            None


def lootjetrekken(indexrange):
    lootjes = list(deelnemers)
    for c in deelnemers:
        combinationcompletion = False
        while combinationcompletion == False:
            getrokkenlootje = random.randrange(0,indexrange)
            if c == lootjes[getrokkenlootje]:
                None
            else:
                print(str(c), "doet een lootje voor", str(lootjes[getrokkenlootje]))
                lootjesdict[str(c)] = str(lootjes[getrokkenlootje])
                del lootjes[getrokkenlootje]
                indexrange -= 1
                combinationcompletion = True    


while names == False:
    naam = input("Schrijf per keer de namen op van de deelnemers. Schrijf alles in kleine letters. Typ 'stop' als alle namen zijn ingetypt. ")
    if naam == "stop":
        names = True
    else:
        nameoverwriteresult = nameoverwritecheck(deelnemers, naam)
        if nameoverwriteresult == True:
            None
        else:
            deelnemers.append(naam)
            aantaldeelnemers += 1

if aantaldeelnemers > 2:
    print("Aantal deelnemers:", aantaldeelnemers)
    print(deelnemers)
    lootjetrekken(aantaldeelnemers)
else:
    print("Niet genoeg deelnemers!")

encodedStr = json.dumps(lootjesdict)
unixtime = int(time.time())
filename = ("data/data_" + str(unixtime) + '.json')
with open(filename, 'x') as file:
    file.write(encodedStr)