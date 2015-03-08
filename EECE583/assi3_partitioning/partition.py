
'''
initialize(blocklist, num_rows, num_cols):
to initialize a gird with random placement, create a grid first (using numpy) and fill it with -1. -1 will mean "empty".
Iterate all blocks:
    While a placement didn't happen yet:
        pick two random numbers (one for x, one for y)
        if(grid[x][y] is empty):
            place the block
            

TODO: remove blocklist            

'''

import numpy
import random
import sys
import math
import plotting
from os import listdir, path

class Partition:

    
    def __init__(self, filename):
        self.filename = filename
        self.netlist, self.blocklist, self.netsOfBlock, self.num_cells, self.num_rows, self.num_cols = self.readfile(filename)
        self.initialize()
    
    '''
    Initialization: create two lists: partA, partB. 
    To populate the partitions, first create a list of consecutive numbers, shuffle the list,
        and then take turns in populating partA and partB
    partA and Part are lists of block NUMBERS
    '''
    def initialize(self):
#         self.costOfNet = numpy.zeros(len(self.netlist), dtype=object)
#         self.location = numpy.empty(len(self.blocklist), dtype=object)
#         self.location.fill(-1);
#         self.grid = numpy.empty((self.num_rows, self.num_cols), dtype=numpy.int32)
#         self.grid.fill(-1)   #this is terrible for performance. I don't need to use a negative number  
        
        #The partitions are lists of block NUMBERS
        self.partA = []
        self.partB = []

        turn = 0;
        #Create list of consecutive numbers
        blocknumbers = [i for i in xrange(self.num_cells)]
        #Shuffle the list of consecutive numbers
        random.shuffle(blocknumbers)
        #Place the shuffled numbers in partA and partB, taking turns
        for i in xrange(0, self.num_cells):
            if(turn == 0):
                self.partA.append(blocknumbers[i])
                turn = 1;
            else:
                self.partB.append(blocknumbers[i])
                turn = 0;
    
#         print self.partA
#         print self.partB
        
#         print self.totalCost()
#         print self.blocklist
        self.totalGain()
        return
    
    
    '''
    The cost function sums the cost of all nets (using costPerNet in a loop)
    Iterate through all NETS:
        calculate costPerNet, add it to totalCost.
    return totalCost
    '''
    def totalCost(self):
        totalCost = 0
        for net in xrange(0, len(self.netlist)):
            cost_net = self.costPerNet(self.netlist[net])
            totalCost += cost_net
#             self.costOfNet[net] = cost_net #add this later if incrementalCost is needed
            print cost_net
        return totalCost
    
    '''
    To calculate cost of specific NET:
    The inputs is the whole net, not just the index
    If all blocks related to this net is in one partition, cost of this net is zero. Otherwise, it's one.
    '''
    def costPerNet(self, net):
        inPartA, inPartB = False, False
        for block in net:
            if block in self.partA:
                inPartA = True
            if block in self.partB:
                inPartB = True
            if(inPartA and inPartB):
                return 1
        return 0
    
    '''
    The gainPerBlock function is defined as the improvement in cut-set size (totalGain) if this block is
        swapped to the opposite partition.
    The input is a block INDEX
    Implementation: find block in blocklist[].
                    locate whether the block is in partA or partB
                    Iterate through relatedBlocks
                        for each related block, find out whether they are in a DIFFERENT partition to the main block
                            if different: gain = gain + 1
    '''
    def gainPerBlock(self, block):
        #Locate where the block is (which partition)
        inPartA, inPartB = False, False
        if block in self.partA:
            inPartA = True
        if block in self.partB:
            inPartB = True

        #Find whether relatedblocks are in same partition
        gain = 0
        for relatedBlock in self.blocklist[block]:
            if (inPartA and relatedBlock in self.partB) or (inPartB and relatedBlock in self.partA):
                gain = gain + 1
        print gain
        return gain
    
    
    def totalGain(self):
        gain = 0
        for blockIndex in xrange(0, len(self.blocklist)):
            gain = gain + self.gainPerBlock(blockIndex)
        print gain
        return gain
    

 
      
    '''
    Input File Format
    The circuit input format is as follows. The first line contains the number of cells to be placed, the number
    of connections between the cells, and the number of rows and columns upon which the circuit should be
    placed. Note that the product of the x and y dimensions should be at least as large as the number of cells in
    the circuit. In the following example, there are 3 cells, 4 connections between the cells, and the circuit
    should be placed on a chip with two rows of two cells each.
    The netlist file then contains one line per net. Each net can connect to two or more logic blocks. For each
    line, the first number is the number of logic blocks to which this net connects. The remaining numbers are
    the block numbers connected to this net. Note that blocks are numbered from 0. 
    
    From the file, we import netlists, but I find it better to represent the data as cell blocks, and each cell block contains the list of blocks it links to.
    (block) is (cell)
    blocklist = [block][list of other blocks it links to]
    How to do it:
    Iterate through all blocks (0 to num_cells):
        Iterate through all netlists:
            if cell exists in net:
                add all blocks in this net to the current block list (except if block_in_net == current_block???). Add to a SET Data Structure. Using Union function
                
    blocklist is a list of SETS
    '''
    def readfile(self, file):
        #Open the benchmark file
        f = open(file, 'r')
        
        #Read the first line: num_cells, num_connections, num_rows, num_cols
        num_cells, num_connections, num_rows, num_cols = [int(x) for x in f.readline().split()] # read first line
    #     print num_cells, num_connections, num_rows, num_cols;
        
        
        #Read the netlist.
        netlist = []
        for net in range(0, num_connections):
            temp = [int(y) for y in f.readline().split()]
            netlist.append(temp[1:])    #ignore the first element (python knows how many elements to read per line, by using the .split() function)
#         print netlist
    
        #Convert the netlist to blocklist
        blocklist = [set() for _ in xrange(num_cells)]
        for block in range (0, num_cells):
            for net in netlist:
                if block in net:
                    blocklist[block] |= set(net)
    #                 print block, net
         
        #Create netsOfBlock: set of all nets related to block
        netsOfBlock = [[] for _ in xrange(num_cells)]
        for block in range (0, num_cells):
            for index, net in enumerate(netlist):
                if block in net:
                    netsOfBlock[block].append(index)
                   
        return netlist, blocklist, netsOfBlock, num_cells, num_rows, num_cols

