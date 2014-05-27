'''
Prova Pratica di Laboratorio di Sistemi Operativi
09 settembre 2002
Esercizio 2

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2002-09-09.pdf

@author: Tommaso Ognibene
'''

import os, sys, re, shutil

def Main(argv):
    # Sanity check
    if len(argv) != 3:
        sys.exit("The function requires two paramenters to be passed in.")
        
    for i in range(1, 3):
        if not os.path.isdir(argv[i]):
            sys.exit("The parameters should be existing directories.")

    CozyJpegDirectory(argv[1], argv[2])
    
    print("Done!")

'''
@summary: Count the number of files within a directory.
'''
def CountFiles(dirPath):
    return sum(1 for item in os.listdir(dirPath) if os.path.isfile(os.path.join(dirPath, item)))

'''
@summary: Pick the Jpeg images within a directory and copy them 
          in a cozy way in the destination directory.
'''
def CozyJpegDirectory(sourceDir, destinationDir):
    index = CountFiles(destinationDir)
    for dirPath, _, fileNames in os.walk(sourceDir):
        for fileName in fileNames:
            extension = os.path.splitext(fileName)[1]
            if extension in ['.jpg', '.jpeg']:
                filePath = os.path.join(dirPath, fileName)
                fileSize = os.path.getsize(filePath)
                if fileSize >= 1024:
                    index += 1
                    destinationPath = os.path.join(destinationDir, str(index) + '.jpg')
                    with open(filePath) as inFile:
                        with open(destinationPath, 'w') as outFile:
                            shutil.copyfileobj(inFile, outFile)
                    
if __name__ == "__main__":
    sys.exit(Main(sys.argv))