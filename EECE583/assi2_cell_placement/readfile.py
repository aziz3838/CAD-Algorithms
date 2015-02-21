
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

import numpy


def read(file):
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

    #Convert the netlist to celllist
    blocklist = [set() for _ in xrange(num_cells)]
    for block in range (0, num_cells):
        for net in netlist:
            if block in net:
                blocklist[block] |= set(net)
#                 print block, net
                
    print blocklist
    return blocklist, num_rows, num_cols