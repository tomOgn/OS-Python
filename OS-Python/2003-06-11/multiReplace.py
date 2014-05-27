'''
Prova Pratica di Laboratorio di Sistemi Operativi
11 giugno 2003
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2003.06.11.pdf

@author: Tommaso Ognibene
'''

import os, sys, shutil

def Main(argv):
    # Sanity check
    if len(argv) < 4:
        sys.exit("The function requires at least three paramenters to be passed in.")

    filePaths = argv[3:]
    for filePath in filePaths:
        if not os.path.isfile(filePath):
            sys.exit(filePath + "is not an existing file.")
        else:
            Replace(filePath, argv[1], argv[2])

    print("Done!")

'''
@summary: Find a replace every occurences of a pattern with a new string in a file.
'''
def Replace(filePath, oldString, newString):
    content = []
    with open(filePath,'r') as file:
        for line in file.readlines():
            content.append(line.replace(oldString, newString))
    with open(filePath, 'w') as file:
        for line in content:
            file.write(line)
                    
if __name__ == "__main__":
    sys.exit(Main(sys.argv))