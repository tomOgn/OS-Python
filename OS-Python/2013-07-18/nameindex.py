'''
Prova Pratica di Laboratorio di Sistemi Operativi
18 luglio 2013
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2013.07.18.pdf

@author: Tommaso Ognibene
'''

import os, sys, errno

'''
@summary: Create a soft link in a forced way.
          If already exists, remove it and create a new one.
@param src: source file
@param dst: destination file
'''
def CreateSoftLink(src, dst):
    try:
        os.symlink(src, dst)
    except OSError as e:
        if e.errno == errno.EEXIST:
            os.remove(dst)
            os.symlink(src, dst)

def Main(argv):
    # Check number of parameters
    if len(argv) != 3:
        sys.exit("The function requires two parameters to be passed in.")
    
    # Check parameters
    srcDir = str(argv[1])
    dstDir = str(argv[2])
    if not os.path.isdir(srcDir):
        sys.exit("First parameter should be an existing directory.")
    if not os.path.isdir(dstDir):
        sys.exit("Second parameter should be an existing directory.")
    
    # Build a dictionary with key-value pair {file base name - occurences}
    nameFreq = { }
    for dirPath, _, fileNames in os.walk(srcDir):
        for fileName in fileNames:
            nameFreq[fileName] = nameFreq.get(fileName, -1) + 1
            
            # Create a soft link
            freq = nameFreq[fileName]
            linkName = "{0}{1}".format(fileName, str(freq) if freq > 0 else "")
            src = os.path.join(os.path.abspath(dirPath), fileName)
            dst = os.path.join(dstDir, linkName)
            CreateSoftLink(src, dst)
        
    print("Done!")

if __name__ == "__main__":
    sys.exit(Main(sys.argv))