import drawing
import itertools
import copy
import random 
def maze(grid, pins):


    temp_grid = copy.deepcopy(grid)
    temp_pins = copy.deepcopy(pins)
    
    
    bestPinsOrder = tryAllPermutations(temp_grid, temp_pins)  
    graphOrder(grid, bestPinsOrder)
    return 0


    
def tryAllPermutations(grid, pins):
    h = len(grid[0])
    w = len(grid)  
    results = []
    tags = [[0 for j in xrange(h)] for i in xrange(w)]
    visited = set()


    #Simple <ulti-Sink. Expand the pins list so it contains two elements per row
    pins_new = []
    wire = []
    index = 0       #the index is to keep track of what wire the two-points belong to.
    while pins:
        temp = pins.pop(0)
        wire[:] = []
        for x in xrange (1, len(temp)):
            wire.append([temp[0], temp[x], index])
        pins_new.extend(wire)   
        index = index + 1
    pins = pins_new
    
    
    
    

        
    sample = []
    if (len(pins) > 5):
        size = 100
        for x in xrange(0, size):
            random.shuffle(pins)
            sample.append(pins)
        option = "small"
    else:
        sample = list(itertools.permutations(pins, len(pins)))
        option = "large"
                
#     print len(sample)
    saved_sample = copy.deepcopy(sample)        
    while sample:
#         drawing.clearTrial(grid)     #Clear the drawing first
        pins = list(sample.pop())
        index = 0
        traceableCount = 0

        temp_grid = copy.deepcopy(grid) 
        number_of_wires = len(pins)

        while pins:
            pin = pins.pop(0)
            queue = [tuple(pin[0])]
            tags[pin[0][0]][pin[0][1]] = 1
            traceable = False
            while queue:
                
                vertex = queue.pop(0)
    #             print vertex, "popped"
    #             print visited
        #         print tuple(vertex)
                if tuple(vertex) not in visited:
    #                 print "not visited"
                    visited.add(tuple(vertex))
                    neigh = neighbours(vertex, h, w, temp_grid, pin[2])
                    queue.extend(neigh)
    #                 print neigh
                    for x in neigh:
                        if tags[x[0]][x[1]] == 0:
                            tags[x[0]][x[1]] = tags[vertex[0]][vertex[1]] + 1
                    for x in neigh:
#                         drawing.printTag(x[0], x[1], tags[x[0]][x[1]])  
    #                     print [x[0]],[x[1]],
    #                     print tags[x[0]][x[1]]
                        if [x[0],x[1]] == pin[1]:
                            traceable = True
                            path = traceBack(tags, pin[1], pin[0], w, h)
#                             drawing.drawWire(path, pin[2])
                            break;
                    if(traceable):
                        break;
        #             drawing.click()            #Enable for very slow speed steps       
#             drawing.click()                    #Enable for intermediate speed steps
            
            if(traceable):
                traceableCount = traceableCount + 1
                for point in path:
                    temp_grid[point[0]][point[1]][0] = 3;    #Setting the state = wire
                    temp_grid[point[0]][point[1]][1] = pin[2]; #Setting "belong to" to wire number
             
            
            #Clear the drawing, Empty the tags list, Empty the visited set
#             drawing.clearTags(temp_grid)     #Clear the drawing first

            tags = [[0 for j in xrange(h)] for i in xrange(w)]
            visited.clear()
            index = index + 1
        
        results.append(traceableCount)

        if traceableCount == number_of_wires:
            break;
    
    maxVal = results[0]
    maxIdx = 0
    for idx, val in enumerate(results):
#         print val
        if maxVal < val:
            maxVal = val
            maxIdx = idx
            
    if(option == "large"):       
        bestResultIndex =  len(sample)-maxIdx-1  
    else:
        bestResultIndex =  maxIdx
    
#     print bestResultIndex
#     print saved_sample

    return saved_sample[bestResultIndex]

def graphOrder(grid, bestPinsOrder):
    
    drawing.draw(grid)
    
    h = len(grid[0])
    w = len(grid)  
    
    tags = [[0 for j in xrange(h)] for i in xrange(w)]
    visited = set()

    

    index = 0

    temp_grid = copy.deepcopy(grid) 
    
    pins = list(bestPinsOrder)
    number_of_pins = len(pins)
    count = 0
#     print pins
    while pins:
        pin = pins.pop(0)
        queue = [tuple(pin[0])]
        tags[pin[0][0]][pin[0][1]] = 1
        traceable = False
        while queue:
            
            vertex = queue.pop(0)
#             print vertex, "popped"
#             print visited
    #         print tuple(vertex)
            if tuple(vertex) not in visited:
#                 print "not visited"
                visited.add(tuple(vertex))
                neigh = neighbours(vertex, h, w, temp_grid, pin[2])
                queue.extend(neigh)
#                 print neigh
                for x in neigh:
                    if tags[x[0]][x[1]] == 0:
                        tags[x[0]][x[1]] = tags[vertex[0]][vertex[1]] + 1
                for x in neigh:
                    drawing.printTag(x[0], x[1], tags[x[0]][x[1]])  
#                     print [x[0]],[x[1]],
#                     print tags[x[0]][x[1]]
                    if [x[0],x[1]] == pin[1]:
                        count = count + 1
                        traceable = True
                        path = traceBack(tags, pin[1], pin[0], w, h)
                        drawing.click() 
                        drawing.drawWire(path, pin[2])
                        break;
                if(traceable):
                    break;
    #             drawing.click()            #Enable for very slow speed steps       
#             drawing.click()                    #Enable for intermediate speed steps
        
        if(traceable):
            for point in path:
                temp_grid[point[0]][point[1]][0] = 3;    #Setting the state = wire
                temp_grid[point[0]][point[1]][1] = pin[2]; #Setting "belong to" to wire number
         
        
        #Clear the drawing, Empty the tags list, Empty the visited set
        drawing.click()
        drawing.clearTags(temp_grid)     #Clear the drawing first
        
        tags = [[0 for j in xrange(h)] for i in xrange(w)]
        visited.clear()
        index = index + 1
        
        
    print count,
    print "segments were routed",
    print "out of",
    print number_of_pins 
    return tags   

def traceBack(tags, source, destination, w, h):

    
    path = []
    path.append(source)
    
    count = tags[source[0]][source[1]]
    count = count - 1
    block = [source[0], source[1]]
    for x in xrange(count, 0, -1):
        #There's left
        if block[0] > 0:
            if tags[block[0]-1][block[1]] == x:
                new_block = [block[0]-1, block[1]]
        if block[0] < w - 1:
            if tags[block[0]+1][block[1]] == x:
                new_block = [block[0]+1, block[1]]
        if block[1] > 0:
            if tags[block[0]][block[1]-1] == x:
                new_block = [block[0], block[1]-1]
        if block[1] < h - 1:
            if tags[block[0]][block[1]+1] == x:
                new_block = [block[0], block[1]+1]
        path.append(new_block)
        block = new_block
    
    return path    
    
def neighbours(vertex, h, w, grid, wire_number):
    blocks = []
    
    #Add left
    if vertex[0] > 0:
        if grid[vertex[0]-1][vertex[1]][0] == 0 or (grid[vertex[0]-1][vertex[1]][0] == 2 and grid[vertex[0]-1][vertex[1]][1] == wire_number) or (grid[vertex[0]-1][vertex[1]][0] == 3 and grid[vertex[0]-1][vertex[1]][1] == wire_number):
            blocks.append([vertex[0]-1, vertex[1]])
        
    #Add right
    if vertex[0] < w - 1:
        if grid[vertex[0]+1][vertex[1]][0] == 0 or (grid[vertex[0]+1][vertex[1]][0] == 2 and grid[vertex[0]+1][vertex[1]][1] == wire_number) or (grid[vertex[0]+1][vertex[1]][0] == 3 and grid[vertex[0]+1][vertex[1]][1] == wire_number):
            blocks.append([vertex[0]+1, vertex[1]])    
    
    #Add top
    if vertex[1] > 0:
        if grid[vertex[0]][vertex[1]-1][0] == 0 or (grid[vertex[0]][vertex[1]-1][0] == 2 and grid[vertex[0]][vertex[1]-1][1] == wire_number) or (grid[vertex[0]][vertex[1]-1][0] == 3 and grid[vertex[0]][vertex[1]-1][1] == wire_number):
            blocks.append([vertex[0], vertex[1]-1])
        
    #Add bottom
    if vertex[1] < h - 1:
        if grid[vertex[0]][vertex[1]+1][0] == 0 or (grid[vertex[0]][vertex[1]+1][0] == 2 and grid[vertex[0]][vertex[1]+1][1] == wire_number) or (grid[vertex[0]][vertex[1]+1][0] == 3 and grid[vertex[0]][vertex[1]+1][1] == wire_number):
            blocks.append([vertex[0], vertex[1]+1])
        
    #CHECK NO OBSTACLES

    return blocks