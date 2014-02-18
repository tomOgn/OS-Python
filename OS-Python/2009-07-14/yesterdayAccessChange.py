'''
Prova Pratica di Laboratorio di Sistemi Operativi
14 luglio 2009
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2009.07.14.pdf

@author: Tommaso Ognibene
'''

import os, sys, datetime, time

def Main(argv):
    # Verify preconditions
    Preconditions(argv)
    
    # Change access time for each file in topDir
    topDir = argv[1]
    WalkDirectories(topDir)
    
    print("Done!")

def Preconditions(argv):
    # Check number of arguments
    if len(argv) != 2:
        print("The function requires one argument to be passed in.")
        return
    
    # Check input directories
    if not (os.path.isdir(argv[1])):
        print("First argument should be an existing directory.")
        return;

# Traverse a directory tree
def WalkDirectories(topDir):
    for dirPath, dirNames, fileNames in os.walk(topDir):
        for fileName in fileNames:
            filePath = os.path.join(dirPath, fileName)
            ChangeAccessTime(filePath)
            
# Change Access Time attribute of a file      
def ChangeAccessTime(filePath):
    now = time.mktime(datetime.datetime.today().timetuple())
    oneDay = 24 * 60 * 60
    yesterday = now - oneDay
    os.utime(filePath, (yesterday, now))

if __name__ == "__main__":
    sys.exit(Main(sys.argv))