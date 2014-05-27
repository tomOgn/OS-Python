#!/usr/local/bin/python3
'''
Prova Pratica di Laboratorio di Sistemi Operativi
25 luglio 2005
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2005.07.25.pdf

@author: Tommaso Ognibene
'''

import os, sys, re

def Average(numbers):
    return sum(numbers) / float(len(numbers))

def Main(argv, argc):
    # Sanity checks
    if argc < 3:
        sys.exit("The function requires at least two parameters to be passed in.")
    
    if not os.path.isfile(argv[1]):
        sys.exit("The first parameter should be an existing file.")  
    
    numColumns = argc - 2
    columns = argv[2 : ]
    for i in range(numColumns):
        if not columns[i].isdigit():
            sys.exit("The other parameters should be natural numbers.")  
    
    # Build a matrix to hold the values of each chosen column
    values = [[] for i in range(numColumns)]
    
    # Populate the matrix
    with open(argv[1]) as file:   
        for line in file:
            match = re.findall('\d+', line) 
            if match:
                for i in range(numColumns):
                    value = int(match[int(columns[i]) - 1])
                    values[i].append(value)
    
    # Compute and display the statistics
    for i in range(numColumns):
        print(str(columns[i]) + ":" +
              " min:" + str(min(values[i])) +
              " max:" + str(max(values[i])) +
              " avg:" + str(Average(values[i])))
    
    print("Done!")
           
if __name__ == "__main__":
    sys.exit(Main(sys.argv, len(sys.argv)))