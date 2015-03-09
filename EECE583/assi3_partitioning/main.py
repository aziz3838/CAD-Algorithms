'''
Created on Mar 08, 2015

@author: Abdulaziz Alghamdi
'''

from partition import *
import sys, getopt
from os import listdir, path
import time

def main(): 
    measurePerformanceOneBench();


'''
This function goes through all benchmarks, and executes Simulated Annealing on each one of them. 
It keeps a record of time for each benchmark. It also shows a graph of the Cost vs. Iterations after EACH benchmark.
The code will STOP until the graph for the current bemchmark is closed.
'''
def measurePerformance():
    benchmarks = listdir("benchmarks")
    totalCost = 0;
    for bench in benchmarks:
        start_time = time.time()
        A = Partition('benchmarks/' + bench)
#         localCost = A.simulatedAnnealing()
        localCost, plot = A.simulatedAnnealingIncrementalCost()
        print path.splitext(path.basename(bench))[0], "\t", localCost
        totalCost += localCost
        print("%s seconds" % (time.time() - start_time))
        
        #graph
        plotting.plot(path.splitext(path.basename(bench))[0], plot)
    
    print "Overall Average\t", totalCost/len(benchmarks) 



def measurePerformanceOneBench():
    start_time = time.time()
    A = Partition('benchmarks/paira.txt')
    localCost = A.partition()
    print "Cost\t", localCost
    print("%s seconds" % (time.time() - start_time))



main()