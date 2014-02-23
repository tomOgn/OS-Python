''' Prova Pratica di Laboratorio di Sistemi Operativi
24 settembre 2003
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2003.09.24.pdf

@author: Tommaso Ognibene  
'''

import os, sys, hashlib, tarfile, gzip

'''
@summary: Compress a file in the TAR format.
@param srcPath: the file path
@return: dstPath: the destination path
'''
def CompressTarFile(srcPath):
    prefix, _ = os.path.splitext(srcPath)
    dstPath = prefix + ".tar.gz"
    
    with tarfile.open(dstPath, "w:gz") as tar:
        tar.add(srcPath, arcname=os.path.basename(srcPath))
        
    return dstPath

'''
@summary: Compress a file in the ZIP format.
@param srcPath: the file path
@return: dstPath: the destination path
'''
def CompressGZipFile(srcPath):
    prefix, _ = os.path.splitext(srcPath)
    dstPath = prefix + ".gz"
        
    with open(srcPath, 'rb') as srcFile:
        with gzip.open(dstPath, 'wb') as dstFile:
            dstFile.writelines(srcFile)
    
    return dstPath

def Main(argv, argc):
    # Pre-conditions:
    # [1] Check number of parameters
    if argc != 2:
        sys.exit("The function requires one parameter to be passed in.")
    
    # [2] Check parameters
    inputDir = argv[1]
    if not (os.path.isdir(inputDir)):
        sys.exit("The paramenter should be an existing directory.")
    
    # Iterate files in the directory
    for fileName in os.listdir(inputDir):
        srcPath = os.path.join(inputDir, fileName)
        dstPath = CompressGZipFile(srcPath)
        if (os.path.getsize(dstPath) < os.path.getsize(srcPath) * 0.5):
            os.remove(srcPath)
        
    print("Done!")
                    
if __name__ == "__main__":
    sys.exit(Main(sys.argv, len(sys.argv)))