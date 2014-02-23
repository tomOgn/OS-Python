'''
Prova Pratica di Laboratorio di Sistemi Operativi
14 luglio 2009
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2009.07.14.pdf

@author: Tommaso Ognibene
'''

import os, sys, datetime, time

def Main(argv):
    # Check number of parameters
    if len(argv) != 2:
        sys.exit("The function requires one parameter to be passed in.")
    
    # Check parameters
    topDir = argv[1]
    if not (os.path.isdir(topDir)):
        sys.exit("First parameter should be an existing directory.")
        
    # Traverse a directory tree
    for dirPath, _, fileNames in os.walk(topDir):
        for fileName in fileNames:
            filePath = os.path.join(dirPath, fileName)
            # Change access time
            ChangeAccessTime(filePath)
            
    print("Done!")

'''
@summary: Change Access Time attribute of a file.
@param filePath: the file path
'''  
def ChangeAccessTime(filePath):
    now = time.mktime(datetime.datetime.today().timetuple())
    oneDay = 24 * 60 * 60
    yesterday = now - oneDay
    os.utime(filePath, (yesterday, now))

if __name__ == "__main__":
    sys.exit(Main(sys.argv))