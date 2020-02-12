import os
import PyPDF2
from shutil import copyfile
parent_dir = '/data1/dbashir/Project/score_scrape/results/composer/'

#composerNames = ['Chopin', 'Bach Sebastian','Liszt','Beethoven','Mozart Amadeus','Rachmaninoff','Mendelssohn Felix',
#        'Borodin','Mussorgsky','Grieg','Clementi','Alb Isaac','Bart%C','Richard Strauss','Vivaldi','Ravel',
#        'Aleksandr Scriabin','Erik Satie', 'Robert Schumann', 'Tchaikovsky','Brahms', 'Franz Schubert',
#        'Debussy', 'Saint Camille']
#composerNames = ['Liszt']
composerDir = []
outdir = '/home/dyang/imslp_dataset/pdfs/'
with open('dbComposers.txt') as f:
    lines = f.readlines()
composerNames = [x.split()[0].strip() for x in lines]
for subdir in os.listdir(parent_dir):
    for i in composerNames:
        composerDir.append(i)
        continue
        tmp = i.split()
        check = True
        for j in tmp:
            if j.lower() not in subdir.lower():
                check = False
        if check:
            composerDir.append(os.path.join(parent_dir,subdir))
pianoDirs = []
numScores = 5560
count = 0
r = False
check = 0
composersUsed = []
leeway = 2
for c in composerDir:
    if r:
        if check == leeway:
            break
        check = check + 1
    composersUsed.append(c)
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
                    if lcase == "piano" or lcase == "piano solo" or lcase == "piano (solo)":
                        pianoDirs.append(pieceDir)
                        count = count+1
                        if count >= numScores:
                            r = True
                    break
f = open("composersUsed.txt", "w")
for i in composersUsed:
    f.write(i)
    f.write("\n")
f.close()
counter = 1
for pieceDir in pianoDirs:
    for subdirs,dirs,files in os.walk(pieceDir):
        for fname in files:
            totaldir = pieceDir+os.sep+fname
            if totaldir[-3:]=='pdf':
                try:
                    PyPDF2.PdfFileReader(open(totaldir, "rb"))
                    copyfile(totaldir,outdir + "p"+str(counter)+".pdf")
                    counter = counter+1
                    print(counter)
                    break
                except:
                    continue
print("Total Number of Files:", counter)
