'''
Created on Feb 21, 2015

@author: Abdulaziz Alghamdi
'''

from placement import *
import sys, getopt
from os import listdir, path

def main():
    
    A = Placement('benchmarks/e64.txt')
#     A = Placement('benchmarks/alu2.txt')
    A.initialize()
    print A.simulatedAnnealing()
      
#     print math.exp(-1.0/.2)
    

#     measurePerformance();


def measurePerformance():
    benchmarks = listdir("benchmarks")
    totalCost = 0;
    for bench in benchmarks:
        A = Placement('benchmarks/' + bench)
        A.initialize()
        localCost = A.simulatedAnnealing()
        print path.splitext(path.basename(bench))[0], "\t", localCost
        totalCost += localCost
    
    print "Overall Average\t", totalCost/len(benchmarks) 
    return;

main()