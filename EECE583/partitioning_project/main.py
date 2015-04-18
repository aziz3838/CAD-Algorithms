'''
Created on Mar 08, 2015

@author: Abdulaziz Alghamdi
'''

from partition import *
import sys, getopt
from os import listdir, path
import time

def main(): 
    start_time = time.time()    

#     measurePerformanceKWay();
    measurePerformanceRec();
#     measurePerformanceOneBench();

    print("Overall Runtime: %.1f seconds" % (time.time() - start_time))



'''
This function goes through all benchmarks, and executes Simulated Annealing on each one of them. 
It keeps a record of time for each benchmark. It also shows a graph of the Cost vs. Iterations after EACH benchmark.
The code will STOP until the graph for the current bemchmark is closed.
'''
def measurePerformanceRec():
    benchmarks = listdir("benchmarks")
    totalCost = 0;
    for bench in benchmarks:
        start_time = time.time()
        A = Partition('benchmarks/' + bench)
        print path.splitext(path.basename(bench))[0], "\t"
        localCost = A.partition_recursive(64)
        totalCost += localCost
        print("%.3f seconds" % (time.time() - start_time))
        print "================="
        
        #graph
#         plotting.plot(path.splitext(path.basename(bench))[0], plot, number_of_passes)
    
    print "Overall Average Cutsize: ", totalCost/len(benchmarks) 
    
def measurePerformanceKWay():
    benchmarks = listdir("benchmarks")
    totalCost = 0;
    for bench in benchmarks:
        start_time = time.time()
        A = Partition('benchmarks/' + bench)
        print path.splitext(path.basename(bench))[0], "\t"
        localCost = A.partition_kway(64)
        totalCost += localCost
        print("%.3f seconds" % (time.time() - start_time))
        print "================="
        
        #graph
#         plotting.plot(path.splitext(path.basename(bench))[0], plot, number_of_passes)
    
    print "Overall Average Cutsize: ", totalCost/len(benchmarks) 



def measurePerformanceOneBench():
    #A.setBlocks(list(set().union(partA, partB)))
    start_time = time.time()

    
    
    
    A = Partition('benchmarks/paira.txt')
    A.TEST2_partition_recursive()
    print("%.1f seconds" % (time.time() - start_time))
    
    start_time = time.time()
    A = Partition('benchmarks/paira.txt')
    A.partition_kway_4()
    
    print("%.1f seconds" % (time.time() - start_time))
    
    
    
    
    #graph
#     plotting.plot("paira", plot, number_of_passes)



main()