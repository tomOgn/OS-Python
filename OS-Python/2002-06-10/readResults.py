'''
Prova Pratica di Laboratorio di Sistemi Operativi
10 giugno 2002
Esercizio 2

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2002-06-10.pdf

@author: Tommaso Ognibene
'''

import os, sys, re, shutil

def Main(argv):
    # Sanity check
    if len(argv) != 2:
        sys.exit("The function requires one paramenter to be passed in.")
        
    filePath = argv[1]
    if not os.path.isfile(filePath):
        sys.exit("The parameter should be an existing file.")

    ParseResults2(filePath)
    
    print("Done!")

'''
@summary: Parse University exams results written in a file.
          Pattern to process: VOTO;<Cognome>;<Nome>;<Voto scritto>;<Voto finale>
'''
def ParseResults2(filePath):
    results = []
    with open(filePath, 'r') as file:   
        for line in file.readlines():
            results.append(re.split(';', line))
    order = ["A-L", "M-Z"]
    for group in order:
        sumMarks = numMarks = bestMark = 0
        print("Group " + group)
        for record in results:
            if re.search("^[" + group + "]" , record[1], re.IGNORECASE) != None:
                sumMarks += int(record[3])
                numMarks += 1
                if record[4] > bestMark:
                    bestMark = record[4]
        if numMarks > 0:
            print('Average = ' + str(sumMarks/float(numMarks)))
            print('Best = ' + bestMark)

if __name__ == "__main__":
    sys.exit(Main(sys.argv))