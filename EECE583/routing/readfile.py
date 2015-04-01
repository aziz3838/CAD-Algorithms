
def read():
    f = open('benchmarks/stdcell.infile', 'r')
    w, h = [int(x) for x in f.readline().split()] # read first line
    
    #Obstacles     
    f_obstacles = int(f.readline())
    obstacles = []
    for x in range(0, f_obstacles):
        temp = [int(y) for y in f.readline().split()]
        obstacles.append(temp)
    #Wires   
    f_wires = int(f.readline())
    max_number_of_sinks = 3     #including source
    pins = []
    for x in range(0, f_wires):
        temp = [int(y) for y in f.readline().split()]
        f_pins = temp[0]
        pins_for_wire = []
        for y in range(0, f_pins):
            pin_x = temp[1+(2*y)]
            pin_y = temp[1+(2*y)+1]
            pins_for_wire.append([pin_x, pin_y])
        pins.append(pins_for_wire)

    #Define Gird List
    grid = [[[0 for k in xrange(2)] for j in xrange(h)] for i in xrange(w)]
    #Add Obstacles to Grid
    for x in obstacles:
        grid[x[0]][x[1]][0] = 1
    #Add Pins to Grid
    for idx, x in enumerate(pins):
        for idx2, x2 in enumerate(pins[idx]):
            grid[x2[0]][x2[1]][0] = 2
            grid[x2[0]][x2[1]][1] = idx
    
    f.close()
    return grid, pins