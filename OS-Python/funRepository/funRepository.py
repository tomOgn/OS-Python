''' FUN-ctions Repository

@summary: A repository of modular functions to be re-used
@author: Tommaso Ognibene
@version: 2014-02-14
'''

import os, errno, hashlib, operator, filecmp, datetime, time, re, tarfile, gzip

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
@summary: Check if two files have same content.
@param f1: file number 1
@param f2: file number 2
@return: TRUE, if they have same content
         FALSE, else
'''
def SameContent(f1, f2):
    if GetMd5Hash(f1) == GetMd5Hash(f2):
        if filecmp.cmp(f1, f2, shallow = False):
            return True
    return False

'''
@summary: Walk through the directory tree and populate a dictionary 
          with key-value pair {file size - [file names]}.
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
          with key-value pair {MD5 hash - [file names]}.
@param filePaths:   the list of physical addresses
@param sameContent: the dictionary
'''
def PopulateSameContent(filePaths, sameContent):
    for filePath in filePaths:
        md5 = GetMd5Hash(filePath)
        sameContent[md5] = sameContent.get(md5, []) + [filePath]

'''
@summary: Delete files having same content
@param sameContent: dictionary with key-value pair {MD5 digest - [file path]}
'''
def DeleteFiles(sameContent):
    for filePaths in sorted(sameContent.values(), key = len, reverse = True):
        if len(filePaths) < 2: break 
        for filePath in filePaths:
            os.remove(filePath)

'''
@summary:  Walk through the directory tree and populate a dictionary 
           with key-value pair {relative file path - MD5 hash}.
           Find files with same name but different content.
@param topDir:   the root directory
@param fileHash: the dictionary
'''
def CompareDirectories(fileHash, topDir):
    for dirPath, _, fileNames in os.walk(topDir):
        for fileName in fileNames:
            filePath = os.path.join(dirPath, fileName)
            md5 = GetMd5Hash(filePath)
            relativePath = os.path.join(os.path.relpath(dirPath, topDir), fileName)
            if not fileHash.get(relativePath, ""):
                fileHash[relativePath] = md5
            elif fileHash[relativePath] != md5:
                print("[{0}]".format(relativePath))

'''
@summary:  Walk through the directory tree and populate a dictionary 
           with key-value pair {file extension - total size}.
@param topDir:        the root directory
@param extensionSize: the dictionary
'''
def PopulateExtensionSize(topDir, extensionSize):
    for dirPath, _, fileNames in os.walk(topDir):
        for fileName in fileNames:
            # Compute the file extension
            fileExtension = fileName[fileName.find(".") : ]
            
            # Compute the size
            filePath = os.path.join(dirPath, fileName)   
            fileSize = os.path.getsize(filePath)
            
            # Update the dictionary
            extensionSize[fileExtension] = extensionSize.get(fileExtension, 0) + fileSize
            
'''
@summary:  Iterate the soft links in the directory /proc.
           Build a list of the active processes.
@param processes: the list
'''
def PopulateActiveProcesses(processes):
    for pid in os.listdir('/proc'):
        # Check if the soft link is accessible
        if pid.isdigit() and os.access('/proc/' + pid + '/exe', os.R_OK):
            path = os.readlink('/proc/' + pid + '/exe')
            processes.append(pid + ' ' + path)  

'''
@summary:  Get system services from /etc/init.d.
           Populate a dictionary with key-value pair {system service - run levels}.
@param services: the list
'''
def PopulateSystemServices(services):
    # Get system services from /etc/init.d
    for service in os.listdir('/etc/init.d'):
        services.setdefault(service, ())
    
    # Search system services for each run level
    for runLevel in range(0, 6):
        for file in os.listdir('/etc/rc' + str(runLevel)  + '.d'):
            # S20kerneloops ->
            # letter = 'S'
            # number = '20'
            # service = 'kerneloops'
            letter = file[0]
            number = "".join(character for character in file[1:] if character.isdigit())           
            service = file[len(number) + 1:]
            services[service] = services.get(service, ()) + ((letter + str(runLevel)),)

'''
@summary: Represenation of a file
'''
class File(object):
    def __init__(self, lastModification = None, relativePath = None):
        self.lastModification = lastModification
        self.relativePath = relativePath

'''
@summary:  Walk through the directory tree and populate a list of the files.
           Sort list by lastModification attribute in increasing order.
@param topDir: the root directory       
@param files: the list
'''
def PopulateLastModifications(topDir, files):
    for dirPath, _, fileNames in os.walk(topDir):
        for fileName in fileNames:
            filePath = os.path.join(dirPath, fileName)
            lastModification = os.path.getmtime(filePath)
            relativePath = os.path.join(os.path.relpath(dirPath, topDir), fileName)
            files.append(File(lastModification, relativePath))
        files.sort(key = operator.attrgetter("lastModification"), reverse = False)

'''
@summary: Walk through a directory tree.
          Populate a dictionary with key-value pair { file name - directories }.
@param topDir:   the root directory  
@param fileDirs: the dictionary
'''
def PopulateFileDirectories(topDir, fileDirs):
    for dirPath, _, fileNames in os.walk(topDir):
        for fileName in fileNames:
            # Find parent directory
            root = os.path.basename(topDir)
            parent = os.path.basename(dirPath)
            if root == parent: parent = ''
            parent = '/' + parent
            
            # Update dictionary
            fileDirs[fileName] = fileDirs.get(fileName, '') + parent + ' '

'''
@summary: Iterate the files of a directory.
          Populate a dictionary with key-value pair { line - number of characters }.
@param inputDir:   the input directory  
@return: the dictionary
'''
def PopulateDictionaryNumChars(inputDir):
    numChars = { }
    
    for fileName in os.listdir(inputDir):
        filePath = os.path.join(inputDir, fileName)
        lineNumber = 1       
        with open(filePath, 'r') as file:
            for line in file:
                numChars[lineNumber] = numChars.get(lineNumber, 0) + len(line) - 1
                lineNumber = lineNumber + 1
    
    return numChars

'''
@summary: Walk through a directory tree.
          Populate a dictionary with key-value pair 
          { file name - (last modification - directory) }.
          Create soft links of the last modified files in a destination directory.
@param sources:     list of source directories  
@param n:           number of source directories
@param destination: the destination directory
'''
def MergeDirectories(sources, n, destination):
    fileLastMod = {}
    
    for i in range(0, n):
        for fileName in os.listdir(sources[i]):
            filePath = os.path.join(sources[i], fileName)
            lastMod = os.path.getmtime(filePath)
            if fileLastMod.get(fileName, None) == None:
                fileLastMod[fileName] = (lastMod, sources[i])
            elif fileLastMod[fileName][0] < lastMod:
                fileLastMod[fileName] = (lastMod, sources[i])
           
    # Create the soft links
    for key, value in fileLastMod.items():
        srcPath = os.path.join(value[1], key)
        dstPath = os.path.join(destination, key)
        if not os.path.lexists(dstPath):
            os.symlink(srcPath, dstPath)
 
'''
@summary: Iterate the files of a directory.
          Populate a dictionary with key-value pair {pattern - occurences}.
@param patterns:   list of patterns
@param inputDir:   input directory
@param patternOcc: dictionary
'''
def PopulatePatternOcc(patternOcc, patterns, inputDir):
    for pattern in patterns:
        patternOcc.setdefault(pattern, 0);  
      
    for fileName in os.listdir(inputDir):
        filePath = os.path.join(inputDir, fileName)
        with open(filePath) as file:   
            for line in file:
                CountOverlappingMatches(patternOcc, line)   
 
'''
@summary: Walk through the directory tree.
          Get the suffix of each file.
          Populate a dictionary with key-value pair {suffix - [file paths]}.
@param topDir:     the root directory
@param suffixFile: the dictionary
'''
def PopulateSameSuffix(topDir, sameSuffix):
    for dirPath, _, fileNames in os.walk(topDir):
        for fileName in fileNames:
            _, suffix = os.path.splitext(fileName)
            filePath = os.path.join(dirPath, fileName)
            sameSuffix[suffix] = sameSuffix.get(suffix, []) + [filePath]

'''
@summary: Iterate the dictionary.
          Create a directory for every key.
          The value associated to every key is a list of files.
          For each new directory create soft links to these files
@param topDir:     the root directory
@param sameSuffix: the dictionary
'''
def CreateDirectoriesSymLinks(topDir, sameSuffix):
    for key, files in sameSuffix.items():
        dirPath = os.path.join(topDir, key)
        if not os.path.isdir(dirPath):
            os.makedirs(dirPath)
        for src in files:
            fileName = os.path.basename(src)
            dst = os.path.join(dirPath, fileName)         
            CreateSoftLink(src, dst)

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

'''
@summary: Change Access Time attribute of a file.
@param filePath: the file path
'''  
def ChangeAccessTime(filePath):
    now = time.mktime(datetime.datetime.today().timetuple())
    oneDay = 24 * 60 * 60
    yesterday = now - oneDay
    os.utime(filePath, (yesterday, now))
    
'''
@summary: Count the overlapping occurences of a pattern in a text
@param patternDict: dictionary with key-value pair {pattern - occurences}
@param text: text to be processed
'''
def CountOverlappingMatches(patternDict, text):
    start = 0
    for key, _ in patternDict.items():
        reObject = re.compile(key)
        match = reObject.search(text, start)
        while match is not None:
            patternDict[key] = patternDict.get(key, 0) + 1
            start = 1 + match.start()       
            match = reObject.search(text, start)

'''
@summary: Find the overlapping occurences of a pattern in a text.
@param pattern: regular expression patter
@param text: input text
@return: list of the overlapping occurences
'''
def FindOverlappingMatches(pattern, text):
    matches = []
    start = 0
    reObject = re.compile(pattern)
    match = reObject.search(text, start)
    while match is not None:
        matches.append(match.group())
        start = 1 + match.start()       
        match = reObject.search(text, start)
    return matches

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