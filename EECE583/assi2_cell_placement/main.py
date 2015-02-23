'''
Created on Feb 21, 2015

@author: Abdulaziz Alghamdi
'''

from placement import *
import sys, getopt
from os import listdir, path
import time

def main():
    start_time = time.time()    


#     A = Placement('benchmarks/pairb.txt')
#     A.initialize()    
#     print A.simulatedAnnealingIncrementalCost()
    
    measurePerformance();

    print("%s seconds" % (time.time() - start_time))


def measurePerformance():
    benchmarks = listdir("benchmarks")
    totalCost = 0;
    for bench in benchmarks:
        start_time = time.time()
        A = Placement('benchmarks/' + bench)
        A.initialize()
#         localCost = A.simulatedAnnealing()
        localCost = A.simulatedAnnealingIncrementalCost()
        print path.splitext(path.basename(bench))[0], "\t", localCost
        totalCost += localCost
        print("%s seconds" % (time.time() - start_time))
    
    print "Overall Average\t", totalCost/len(benchmarks) 
    return;

main()