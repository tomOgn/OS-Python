'''
Prova Pratica di Laboratorio di Sistemi Operativi
18 febbraio 2003
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2003.02.18.pdf

@author: Tommaso Ognibene
'''

import os, sys, re

def Main(argv):
    # Sanity check
    if len(argv) != 2:
        sys.exit("The function requires one paramenter to be passed in.")

    ParseResults(argv[1])
    
    print("Done!")

'''
@summary: Parse University exams results written in a file.
          Pattern to process: VOTO;<Surname>;<Name>;<Sex>;<Mark>
'''
def ParseResults(filePath):
    results = []
    with open(filePath,'r') as file:   
        for line in file.readlines():
            results.append(re.split(';', line))
    sum = 0.0
    n = 0.0
    order = ['M', 'F']
    for sex in order:
        for record in results:
            if record[3] == sex:
                sum += int(record[4])
                n += 1
                print(record[1] + ' ' + record[2])
        print('Average = ' + str(sum/n))
                    
if __name__ == "__main__":
    sys.exit(Main(sys.argv))