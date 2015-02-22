
'''
initialize(blocklist, num_rows, num_cols):
to initialize a gird with random placement, create a grid first (using numpy) and fill it with -1. -1 will mean "empty".
Iterate all blocks in blocklist:
    While a placement didn't happen yet:
        pick two random numbers (one for x, one for y)
        if(grid[x][y] is empty):
            place the block
            
            

'''

import numpy
import random
import sys
import math


class Placement:

    
    def __init__(self, filename):
        self.netlist, self.blocklist, self.num_rows, self.num_cols = self.readfile(filename)
    
    def initialize(self):
        self.location = numpy.empty(len(self.blocklist), dtype=object)
        self.location.fill(-1);
        self.grid = numpy.empty((self.num_rows, self.num_cols))
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
        
#         print self.grid
#         print self.location
        self.cost = self.totalCost()
#         print self.totalCost()
        return 0
    
    
    
    
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
        calculate costPerNet, add it to totalCost
    return totalCost
    '''
    def totalCost(self):
        totalCost = 0
        for net in xrange(0, len(self.netlist)):
            totalCost += self.costPerNet(self.netlist[net])
        return totalCost
    
    
    def incrementalCost(self):
        return 0
    
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
    This function return whether the input coordinate contains a cellblock or not (empty).
    '''
    def isEmptyPos(self, pos):
        if(self.grid[pos[0]][pos[1]] == -1):
            return True
        return False
    
    def simulatedAnnealing(self):
        
        T = 10;
        while(T > 0.1):
            for x in xrange(0, 100):
                #Pcik two random blocks
                pos1 = (random.randrange(0, self.num_rows), random.randrange(0, self.num_cols))
                pos2 = (random.randrange(0, self.num_rows), random.randrange(0, self.num_cols))
                self.swap(pos1, pos2)
                
                #Cost: needs improvement
                new_cost = self.totalCost()
                old_cost = self.cost
                delta_cost = new_cost - old_cost;
                if(new_cost <= old_cost):    #If solution is better, accept it
                    #update cost
                    self.cost = new_cost
                else:    #solution is worse
                    r = random.random()
#                     print r, math.exp(-delta_cost/T)
                    if(r < math.exp(-delta_cost/T)): #the probability of taking a wrong move
                        #Take the move. #update cost
                        self.cost = new_cost
                    else:
                        #Don't take the move. Reverse the swap
                        self.swap(pos2, pos1)
            T = T - 0.01
#         print self.totalCost()
        return self.totalCost()
    
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
                    
#         print blocklist
        return netlist, blocklist, num_rows, num_cols
    # '''
    # To calculate cost of specific block:
    # Iterate through the blocklist related to the current block(first input):
    #     locate the block (x &y, using the locate function)
    #     find max x & y, min x & y
    # Cost per row (y) is double the columns (x)
    # '''
    # def costPerBlock(blocklist):
    #     max_x, max_y, min_x, min_y =  0, 0, sys.maxint, sys.maxint
    #     for block in blocklist:
    #         y, x = locate(block)    #y is row, x is col
    #         if(x > max_x):
    #             max_x = x
    #         if(y > max_y):
    #             max_y = y
    #         if(x < min_x):
    #             min_x = x
    #         if(y < min_y):
    #             min_y = y
    #             
    #     half_perim_cost = ((max_y - min_y)*2) + (max_x - min_x)
    # #     print min_x, min_y, max_x, max_y
    #     print half_perim_cost
    #     return half_perim_cost 
