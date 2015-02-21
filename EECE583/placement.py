
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

def initialize(blocklist, num_rows, num_cols):
    grid = numpy.empty((num_rows, num_cols))
    grid.fill(-1)   #this is terrible for performance. I don't need to use a negative number
    
    #initialize grid with random placement
    for block_num in range(0, len(blocklist)):
        placed = False;
        while(placed == False):
            row = random.randrange(0, num_rows)
            col = random.randrange(0, num_cols)
            if(grid[row][col] == -1):
                grid[row][col] = block_num
                placed = True
    
    print grid

    return 0