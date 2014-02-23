''' Prova Pratica di Laboratorio di Sistemi Operativi
02 luglio 2003
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2003.07.02.pdf

@author: Tommaso Ognibene  
'''

import os, sys, re

'''
@summary: Count the overlapping occurences of a pattern in a text.
@param patternOcc: dictionary with key-value pair { pattern - occurences }
@param text      : text to be processed
'''
def CountOverlappingMatches(patternOcc, patterns, text):
    start = 0
    for pattern in patterns:
        object = re.compile(pattern)
        match = object.search(text, start)
        while match is not None:
            patternOcc[pattern] += + 1
            start = 1 + match.start()       
            match = object.search(text, start)

'''
@summary: Find the overlapping occurences of a pattern in a text.
@param pattern: regular expression patter
@param text   : input text
@return: list of the overlapping occurences
'''
def FindOverlappingMatches(pattern, text):
    matches = []
    start = 0
    object = re.compile(pattern)
    match = object.search(text, start)
    while match is not None:
        matches.append(match.group())
        start = 1 + match.start()       
        match = object.search(text, start)
    return matches

'''
@summary: Iterate the files of a directory.
          Populate a dictionary with key-value pair {pattern - occurences}.
@param patterns:   list of patterns
@param inputDir:   input directory
@param patternOcc: dictionary
'''
def PopulatePatternOcc(patternOcc, patterns, filePaths):
    for pattern in patterns:
           patternOcc.setdefault(pattern, 0);
           
    for filePath in filePaths:
        with open(filePath) as file:
            for line in file:
                CountOverlappingMatches(patternOcc, patterns, line)

def Main(argv, argc):
    # Pre-conditions:
    # [1] Check number of parameters
    if argc < 3:
        sys.exit("The function requires at least two parameters to be passed in.")
    
    # [2] Check parameters
    inputString = argv[1]
    filePaths = []
    for i in range(2, argc):
        print(argv[i])
        if not os.path.isfile(argv[i]):
            sys.exit("The first paramenters after the string should be existing files.")
        filePaths.append(argv[i])
    [prefix for prefix in prefix_list if word.startswith(prefix)]
    # Get the overlapping patterns from the input string
    lenght = len(inputString)
    pattern = ""
    for i in range(lenght - 1):
        pattern += ".{" + str(i + 1) + "}|"
    pattern += ".{" + str(lenght) + "}"
    print(pattern)
     
    patterns = FindOverlappingMatches(pattern, inputString) 
    print(patterns)
    print(filePaths)
    # Build a dictionary with key-value pair {pattern - occurences}
    patternOcc = {}
    PopulatePatternOcc(patternOcc, patterns, filePaths)
    
    for key, value in patternOcc.items():
        print('{0}\t{1}'.format(key, value))     
        
    print("Done!")     
    
if __name__ == "__main__":
    argv = ["grepPyramidal", "123456", \
            "/home/tommaso/Code/git/OS-Python/OS-Python/2003-07-02/f1", \
            "/home/tommaso/Code/git/OS-Python/OS-Python/2003-07-02/f2"]
    sys.exit(Main(argv, len(argv)))