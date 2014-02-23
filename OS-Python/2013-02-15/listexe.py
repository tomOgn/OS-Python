'''
Prova Pratica di Laboratorio di Sistemi Operativi
15 febbraio 2013
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2013.02.15.pdf

@author: Tommaso Ognibene
'''

import os, sys

def Main(argv):
    # Check number of parameters
    if len(argv) != 1:
        sys.exit("The function does not require parameters to be passed in.")
    
    processes = []
    PopulateActiveProcesses(processes)
    
    # Print results
    print("{0}".format("\n".join(str(process) for process in processes)))

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
    
if __name__ == "__main__":
    sys.exit(Main(sys.argv))