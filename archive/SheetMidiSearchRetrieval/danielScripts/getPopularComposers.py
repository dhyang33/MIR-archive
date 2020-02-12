import os
from shutil import copyfile
parent_dir = '/data1/dbashir/Project/score_scrape/results/composer/'

composerDir = []
outdir = '/home/dyang/imslp_dataset/'

def sortKey(item):
    return item[1]

for subdir in os.listdir(parent_dir):
    cDir = os.path.join(parent_dir,subdir)
    if os.path.isdir(cDir):
        sdir = subdir.strip()
        composerDir.append((sdir,cDir))
pianoDirs = []
composerList = []
for composer,c in composerDir:
    popularity = 0
    for subdir in os.listdir(c):
        if subdir[-3:]=='txt':
            continue
        pieceDir = os.path.join(c,subdir)
        html = pieceDir+os.sep+'html.txt'
        if not os.path.exists(html):
            continue
        with open(html,'r') as fp:
            #line = fp.readline()
            for line in fp:
                if line.strip() == '<th>Instrumentation':
                    fp.readline()
                    instruments = fp.readline()
                    instruments = instruments
                    instruments = instruments[4:]
                    lcase = instruments.lower()
                    lcase = lcase.strip()
                    #print(lcase)
                    if lcase == "piano" or lcase == "piano solo" or lcase == "piano (solo)":
                        pianoDirs.append(pieceDir)
                        popularity = popularity+1
                    break
    composerList.append((c,popularity))
composerList = sorted(composerList,key=sortKey,reverse=True)
counter = 1
f = open("composerFile.txt", "w")
for i in range(len(composerList)):
    f.write(composerList[i][0]+ " " + str(composerList[i][1]))
    f.write("\n")
f.close()

