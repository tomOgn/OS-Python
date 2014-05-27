'''
Prova Pratica di Laboratorio di Sistemi Operativi
27 luglio 2005
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2005.06.27.pdf

@author: Tommaso Ognibene
'''

import os, sys, hashlib, difflib

def main(argv, argc):
    # Sanity check
    if argc < 2:
        sys.exit("The function requires at least one parameter to be passed in.")
    
    for i in range(1, argc):
        if not (os.path.isdir(argv[i])):
            sys.exit("The parameters should be existing directories.")       
        
    # Build a dictionary with key-value pair {file size - [file path]}
    sameSize = { }
    for i in range(1, argc):
        PopulateSameSize(argv[i], sameSize)    
        
    # Build a dictionary with key-value pair {MD5 hash - [file path]}
    sameContent = { }
    for filePaths in sorted(sameSize.values(), key = len, reverse = True):
        if len(filePaths) < 2: break
        PopulateSameContent(filePaths, sameContent)   
             
    # Print results
    PrintResults(sameContent)
    
    print("Done!")
    
'''
@summary: Walk through the directory tree and populate a dictionary 
          with key-value pair {file size - [file paths]}.
@param topDir:   the root directory
@param sameSize: the dictionary
'''
def PopulateSameSize(topDir, sameSize):
    for dirPath, _, fileNames in os.walk(topDir):
        for fileName in fileNames:
            filePath = os.path.join(dirPath, fileName)
            fileSize = os.path.getsize(filePath)
            sameSize[fileSize] = sameSize.get(fileSize, []) + [filePath]
            
'''
@summary: Read a list of file paths and populate a dictionary 
          with key-value pair {MD5 hash - [file paths]}.
@param filePaths:   the list of physical addresses
@param sameContent: the dictionary
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
@param chunkSize: chunk size in Bytes
@return: MD5 digest
'''
def GetMd5Hash(filePath, chunkSize = 2 ** 20):
    digest = hashlib.md5()
    with open(filePath, 'rb') as file:
        chunk = file.read(chunkSize)
        while chunk:
            digest.update(chunk)
            chunk = file.read(chunkSize)
    return digest.hexdigest()

'''
@summary: Printout the lists of files having same content.
@param sameContent: a dictionary with key-value pair {MD5 hash - [file paths]}
'''
def PrintResults(sameContent):
    print("Lists of files having same content:")
    for files in sorted(sameContent.values(), key = len, reverse = True):
        if len(files) < 2: break
        print("[{0}]".format(", ".join(file for file in files)))

if __name__ == "__main__":
    sys.exit(main(sys.argv, len(sys.argv)))