
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

class Placement:

    
    def __init__(self, filename):
        self.filename = filename
        self.netlist, self.blocklist, self.netsOfBlock, self.num_cells, self.num_rows, self.num_cols = self.readfile(filename)
    
    '''
    Initialization: created empty numpy arrays. Initialize grid with random placement
    '''
    def initialize(self):
        self.costOfNet = numpy.zeros(len(self.netlist), dtype=object)
        self.location = numpy.empty(len(self.blocklist), dtype=object)
        self.location.fill(-1);
        self.grid = numpy.empty((self.num_rows, self.num_cols), dtype=numpy.int32)
        self.grid.fill(-1)   #this is terrible for performance. I don't need to use a negative number  
        #initialize grid with random placement
        for block_num in xrange(0, len(self.blocklist)):
            placed = False;
            while(placed == False):
                row = random.randrange(0, self.num_rows)
                col = random.randrange(0, self.num_cols)
                if(self.grid[row][col] == -1):
                    self.place(block_num, row, col)
                    placed = True
    
        self.cost = self.totalCost()
        return
    
    
    
    
    '''
    To calculate cost of specific NET:
    Iterate through the blocks in the net:
        locate the block (x &y, using the locate function)
        find max x & y, min x & y
    Cost per row (y) is double the columns (x)
    '''
    def costPerNet(self, net):
        max_x, max_y, min_x, min_y =  0, 0, sys.maxint, sys.maxint
        for block in net:
            y, x = self.locate(block)    #y is row, x is col
    #         print x, y
            if(x > max_x):
                max_x = x
            if(y > max_y):
                max_y = y
            if(x < min_x):
                min_x = x
            if(y < min_y):
                min_y = y
                
        half_perim_cost = ((max_y - min_y)*2) + (max_x - min_x)
    #     print min_x, min_y, max_x, max_y
    #     print half_perim_cost
        return half_perim_cost
    
    '''
    To calculate initial total cost:
    Iterate through all NETS:
        calculate costPerNet, add it to totalCost. Also, add the cost to the list costOfNet[]
    return totalCost
    '''
    def totalCost(self):
        totalCost = 0
        for net in xrange(0, len(self.netlist)):
            cost_net = self.costPerNet(self.netlist[net])
            totalCost += cost_net
            self.costOfNet[net] = cost_net
#         print self.costOfNet
        return totalCost
    
    
    
    '''
    locate(x, y):
    this function helps make cost calculation easier. The same information can be retrieved by looking at the grid list.
    '''
    def locate(self, block):
        row = self.location[block][0]
        col = self.location[block][1]
        return row, col
    
    '''
    Basically, gird & location are the reverse of each other. So, they should be update together all the time. Therefore: def place(block)num, row, col)
    '''
    def place(self, block_num, row, col):
        self.grid[row][col] = block_num
        self.location[block_num] = (row, col)
        return
    
    '''
    Inputs: grid POSITIONS. This is important, becase we need to include empty cells in our swaps
    we need to update both grid, and location. We cannot use "place", because some blocks are empty
    '''
    def swap(self, pos1, pos2):
        #If both positions are empty cells, exit function
        if(self.isEmptyPos(pos1) and self.isEmptyPos(pos2)):
            return
        
        block_in_pos1 = self.grid[pos1[0]][pos1[1]]
        block_in_pos2 = self.grid[pos2[0]][pos2[1]]
            
        #Update Location. Be careful with how the swap is happening
        #If position2 is not empty (contains block), then, block2: position1 is your new position.
        if(not self.isEmptyPos(pos2)):
            self.location[block_in_pos2] = (pos1[0], pos1[1])
        if(not self.isEmptyPos(pos1)):
            self.location[block_in_pos1] = (pos2[0], pos2[1])

 
        #Update grid:
        self.grid[pos1[0]][pos1[1]] = block_in_pos2
        self.grid[pos2[0]][pos2[1]] = block_in_pos1

        return;
    '''
    First, find related nets, and get their cost from costOfNet[].
    Update the cost with new cost calculated by calling costPerNet(net)
    Get deltaCost. return negative if good move, positive if bad.
    '''
    def updateCostOfSwap(self, pos1, pos2):
        #If both positions are empty cells, return 0
        if(self.isEmptyPos(pos1) and self.isEmptyPos(pos2)):
#             self.counter = self.counter + 1
            return 0
        
        #Find related nets
        block_in_pos1 = self.grid[pos1[0]][pos1[1]]
        block_in_pos2 = self.grid[pos2[0]][pos2[1]]
        nets1, nets2 = [], []
        if(not self.isEmptyPos(pos1)):
            nets1 = self.netsOfBlock[block_in_pos1]
        if(not self.isEmptyPos(pos2)):
            nets2 = self.netsOfBlock[block_in_pos2]
        relatedNets = list(set(nets1 + nets2))
        
        #Find cost of related nets from saved list (costOfNet[])
        oldCostOfRelatedNets = 0
        for net in relatedNets:
            oldCostOfRelatedNets += self.costOfNet[net]
            
        #update cost of related nets in costOfNet[]
        newCostOfRelatedNets = 0
        for net in relatedNets:
            cost_new = self.costPerNet(self.netlist[net])   #need to pass the whole net costPerNet, not just its number
            self.costOfNet[net] = cost_new
            newCostOfRelatedNets += cost_new
        
        #deltaCost is negative if good move, positive if bad.
        deltaCost =  newCostOfRelatedNets - oldCostOfRelatedNets
        return deltaCost
    
    '''
    This function return whether the input coordinate contains a cellblock or not (empty).
    '''
    def isEmptyPos(self, pos):
        if(self.grid[pos[0]][pos[1]] == -1):
            return True
        return False
    
#     def simulatedAnnealing(self):    
#         T = 10;
#         while(T > 0.1):
#             for x in xrange(0, 100):
#                 #Pcik two random blocks
#                 pos1 = (random.randrange(0, self.num_rows), random.randrange(0, self.num_cols))
#                 pos2 = (random.randrange(0, self.num_rows), random.randrange(0, self.num_cols))
#                 self.swap(pos1, pos2)
#                 
#                 #Cost: needs improvement
#                 new_cost = self.totalCost()
#                 old_cost = self.cost
#                 delta_cost = new_cost - old_cost;
#                 if(new_cost <= old_cost):    #If solution is better, accept it
#                     #update cost
#                     self.cost = new_cost
#                 else:    #solution is worse
#                     r = random.random()
# #                     print r, math.exp(-delta_cost/T)
#                     if(r < math.exp(-delta_cost/T)): #the probability of taking a wrong move
#                         #Take the move. #update cost
#                         self.cost = new_cost
#                     else:
#                         #Don't take the move. Reverse the swap
#                         self.swap(pos2, pos1)
#             T = T - 0.01
# #         print self.totalCost()
#         return self.totalCost()
 
    '''
    Simulated Annealing Algorithm.
    '''
    def simulatedAnnealingIncrementalCost(self):  
        #Initialize Graph
#         hl = plotting.graph(path.splitext(path.basename(self.filename))[0])
        
        plot = []
        start = 7
        step = 0.0001
        T = start;
        while(T > 0.0001):
            pickRandomness_row = int(((T/4/step)/(start/step)) * self.num_rows) + 2
            pickRandomness_col = int(((T/4/step)/(start/step)) * self.num_cols) + 3
            
            innerIterations = int((start - T)*1.5 + 4) #more innerIterations at the end
            for x in xrange(0, innerIterations):
                #Pick two random blocks
                pos1, pos2 = self.pickTwoPositions(pickRandomness_row, pickRandomness_col)
                
                self.swap(pos1, pos2)
                delta_cost = self.updateCostOfSwap(pos2, pos1)
                self.cost += delta_cost
                #If move is good (negative). Do nothing. Do not reverse the swap.
                if(delta_cost > 0):    #If solution is worse
                    r = random.random()
#                     print r, math.exp(-delta_cost/T)
                    #The probability of taking a wrong move. If take the move. Do nothing. Do not reverse the swap.
                    if(r > math.exp(-delta_cost/T)): 
                        #Don't take the move. Reverse the swap
                        self.swap(pos2, pos1)
                        delta_cost = self.updateCostOfSwap(pos1, pos2)
                        self.cost += delta_cost
                 
            T = T - step
            plot.append(self.cost)
        
        return self.cost , plot
    
    '''
    Picking positions is random, but it can be optimized by making it less random.
    Instead of picking positions that can be far from each other, we can limit this by:
        pos1 is chosen randomly. OR pos1 is a position for a block that we already know (using locate())
        pos2 is chosen randomly, but limited to a few positions close to pos1
    '''
    def pickTwoPositions(self, pickRandomness_row, pickRandomness_col):
#         pos1 = (random.randrange(0, self.num_rows), random.randrange(0, self.num_cols))
#         pos2 = (random.randrange(0, self.num_rows), random.randrange(0, self.num_cols))
        
        #Picking two positions close to each other
        pos1 = self.locate(random.randrange(0, self.num_cells))
        t_pos2 = [0, 0]
        t_pos2[0] = random.randrange(0, pos1[0]+pickRandomness_row)
        t_pos2[1] = random.randrange(0, pos1[1]+pickRandomness_col)
         
        if(t_pos2[0] >= self.num_rows):
            t_pos2[0] = self.num_rows - 1  
        if(t_pos2[1] >= self.num_cols):
            t_pos2[1] = self.num_cols - 1   
        pos2 = (t_pos2[0], t_pos2[1])
        return pos1, pos2
      
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
    #     print netlist
    
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

