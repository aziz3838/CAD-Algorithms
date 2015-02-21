
'''
initialize(blocklist, num_rows, num_cols):
to initialize a gird with random placement, create a grid first (using numpy) and fill it with -1. -1 will mean "empty".
Iterate all blocks in blocklist:
    While a placement didn't happen yet:
        pick two random numbers (one for x, one for y)
        if(grid[x][y] is empty):
            place the block
            
            
locate(x, y):
this function helps make cost calculation easier. The same information can be retrieved by looking at the grid list.
Basically, gird & location are the reverse of each other. So, they should be update together all the time. Therefore: def place(block)num, row, col)
'''

import numpy
import random
import sys
grid, location = 0, 0
def initialize(blocklist, num_rows, num_cols):
    global grid, location
    location = numpy.empty(len(blocklist), dtype=object)
    location.fill(-1);
    grid = numpy.empty((num_rows, num_cols))
    grid.fill(-1)   #this is terrible for performance. I don't need to use a negative number
    
    #initialize grid with random placement
    for block_num in range(0, len(blocklist)):
        placed = False;
        while(placed == False):
            row = random.randrange(0, num_rows)
            col = random.randrange(0, num_cols)
            if(grid[row][col] == -1):
                place(block_num, row, col)
                placed = True
    
    print grid
    print location
    
    print initialTotalCost(blocklist)

    return 0


'''
To calculate cost of specific block:
Iterate through the blocklist related to the current block(first input):
    locate the block (x &y, using the locate function)
    find max x & y, min x & y
Cost per row (y) is double the columns (x)
'''
def costPerBlock(blocklist):
    max_x, max_y, min_x, min_y =  0, 0, sys.maxint, sys.maxint
    for block in blocklist:
        y, x = locate(block)    #y is row, x is col
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
    print half_perim_cost
    return half_perim_cost

def initialTotalCost(blocklist):
    totalCost = 0
    for block in range(0, len(blocklist)):
        totalCost += costPerBlock(blocklist[block])
    return totalCost

def incrementalCost():
    return 0

def locate(block):
    row = location[block][0]
    col = location[block][1]
    return row, col

def place(block_num, row, col):
    global grid, location
    grid[row][col] = block_num
    location[block_num] = (row, col)
    return