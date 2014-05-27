'''
Prova Pratica di Laboratorio di Sistemi Operativi
31 gennaio 2003
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2003.01.31.pdf

@author: Tommaso Ognibene
'''

import os, sys, re

def Main(argv):
    # Sanity check
    if len(argv) != 3:
        sys.exit("The function requires two paramenters to be passed in.")
    dirPath = argv[1]
    if not os.path.isdir(dirPath):
        sys.exit("The first parameter should be an existing directory.")
    commentPath = argv[2]
    if not os.path.isfile(commentPath):
        sys.exit("The second parameter should be an existing file.")
        
    comment = open(commentPath).read()
    for fileName in os.listdir(dirPath):
        filePath = os.path.join(dirPath, fileName)
        AddComment(filePath, comment)
    
    print("Done!")

'''
@summary: Add a comment to the beginning of a file if the file is not protected by copyright.
'''
def AddComment(filePath, comment):
    content = open(filePath).read()
    if not re.search('copyright', content, re.IGNORECASE):
        with open(filePath, 'w') as writeFD:
            writeFD.write(comment)
            writeFD.write(content)
                    
if __name__ == "__main__":
    sys.exit(Main(sys.argv))