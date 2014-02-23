''' Prova Pratica di Laboratorio di Sistemi Operativi
24 settembre 2004
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2004.09.24.pdf

@author: Tommaso Ognibene  
'''

import os, sys, hashlib

'''
@summary: Populate a dictionary in order to associate files having same content
@param filePaths: list of the physical addresses of the files
@param sameContent: dictionary with key-value pair {MD5 digest - [file path]}
'''
def PopulateSameContent(filePaths, sameContent):
    for filePath in filePaths:
        md5 = GetMd5Hash(filePath)
        sameContent[md5] = sameContent.get(md5, []) + [filePath]

'''
@summary: Get the MD5 hash without loading the whole file to memory.
          Break the file in chunks whose size is a multiple of 128.
          This takes advantage of the fact that MD5 has 128-byte digest blocks.
@param filePath:  physical address of a file 
@param blockSize: chunks size in Bytes
@return: MD5 digest
'''
def GetMd5Hash(filePath, blockSize = 2 ** 20):
    digest = hashlib.md5()
    with open(filePath, "rb") as file:
        for chunk in iter(lambda: file.read(blockSize), b''): 
            digest.update(chunk)
    return digest.hexdigest()

'''
@summary: Populate a dictionary in order to associate files having same size
@param inputDir: physical address of the input directory
@param sameSize: dictionary with key-value pair {file size - [file path]}
'''
def PopulateSameSize(inputDir, sameSize):
    for dirPath, _, fileNames in os.walk(inputDir):
        for fileName in fileNames:
            filePath = os.path.join(dirPath, fileName)
            fileSize = os.path.getsize(filePath)
            sameSize[fileSize] = sameSize.get(fileSize, []) + [filePath]

'''
@summary: Delete files having same content
@param sameContent: dictionary with key-value pair {MD5 digest - [file path]}
'''
def DeleteFiles(sameContent):
    for filePaths in sorted(sameContent.values(), key = len, reverse = True):
        if len(filePaths) < 2: break 
        for filePath in filePaths:
            os.remove(filePath)

def Main(argv, argc):
    # Pre-conditions:
    # [1] check number of arguments
    if argc != 3:
        sys.exit("The function requires two parameters to be passed in.")
    
    # [2] check parameters
    for i in range(2):
        if not os.path.isdir(argv[i + 1]):
            sys.exit("The parameters should be two existing directories.")
    
    # Build a dictionary with key-value pair {file size - [file name]}
    sameSize = { }
    PopulateSameSize(argv[1], sameSize)
    PopulateSameSize(argv[2], sameSize)
    
    # Build a dictionary with key-value pair {MD5 hash - [file name]}
    sameContent = { }
    for filePaths in sorted(sameSize.values(), key = len, reverse = True):
        # No files with same size => No files with same content
        if len(filePaths) < 2: break
        PopulateSameContent(filePaths, sameContent)    
    
    DeleteFiles(sameContent)
    
    print("Done!")
                    
if __name__ == "__main__":
    sys.exit(Main(sys.argv, len(sys.argv)))