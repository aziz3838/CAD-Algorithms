from graphics import *

from itertools import cycle
from mhlib import PATH
w, h, win, winsize, colours = 0, 0, 0, 0, 0

def draw(grid):
    global h, w, win, winsize, colours
    h = len(grid[0])
    w = len(grid)     
#     print h, w,   
    colours = ['red', 'green', 'yellow', 'purple', 'black', 'Lime', 'Cyan', 'PeachPuff']
    #Draw Graph Window Grid.
    winsize = 800

    win = GraphWin("Aziz's Router", winsize, int(winsize*(float(h)/w)))

    drawSquares(colours)   
    #Draw Obstacles (from grid list)
    for i in range(w):
        for j in range(h):
            if grid[i][j][0] == 1:
                paintObstacle(i, j)
    #Draw Pins (from grid list)
    for i in range(w):
        for j in range(h):
            if grid[i][j][0] == 2:
                paintPin(i, j, colours[grid[i][j][1]])     #Color is assigned by pin_belong_to_wire variable in grid
                
    #Draw tags (from tags list)
#     for i in range(w):
#         for j in range(h):
#             if tags[i][j] != 0:
#                 printTag(i, j, tags[i][j])     #Color is assigned by pin_belong_to_wire variable in grid
#                 win.getMouse()
                
    win.getMouse()
#     win.close()  
    
def drawSquares(colours):
    global h, w, win, winsize
    gsize = max(h,w)
    side = winsize / gsize
    color = cycle(colours)
    for row in range(h):
        y1 = row * side
        y2 = y1 + side
        for column in range(w):
            x1 = column * side
            x2 = x1 + side
            rect = Rectangle(Point(x1, y1), Point(x2, y2))
            rect.setFill('white')
            rect.draw(win)


def paintObstacle(x, y):
    global h, w, win, winsize
    gsize = max(h,w)
    side = winsize / gsize

    y1 = y * side
    y2 = y1 + side

    x1 = x * side
    x2 = x1 + side
    rect = Rectangle(Point(x1, y1), Point(x2, y2))
    rect.setFill('blue')
    rect.draw(win)
    
def paintPin(x, y, color):
    global h, w, win, winsize
    gsize = max(h,w)
    side = winsize / gsize

    y1 = y * side
    y2 = y1 + side

    x1 = x * side
    x2 = x1 + side
    rect = Rectangle(Point(x1, y1), Point(x2, y2))
    rect.setFill(color)
    rect.draw(win)
    
def printTag(x, y, tag):
    global h, w, win, winsize
    gsize = max(h,w)
    side = winsize / gsize
    y1 = y * side
    y2 = y1 + side/2
    x1 = x * side
    x2 = x1 + side/2
    text = Text(Point(x2, y2), tag)
    text.draw(win)
    
    
def drawWire(path, color):
    global h, w, win, winsize, colours
    gsize = max(h,w)
    side = winsize / gsize
    for point in path:
        x = point[0]
        y = point[1]
        y1 = y * side
        y2 = y1 + side
        x1 = x * side
        x2 = x1 + side
        rect = Rectangle(Point(x1, y1), Point(x2, y2))
        rect.setFill(colours[color])
        rect.draw(win)
        
    
def clearTags(grid):
    global h, w, win, winsize, colours
    gsize = max(h,w)
    side = winsize / gsize
    color = cycle(colours)
    for row in range(h):
        y1 = row * side
        y2 = y1 + side
        for column in range(w):
            x1 = column * side
            x2 = x1 + side
            if(grid[column][row][0] == 0):      #Clear the FREE blocks
                rect = Rectangle(Point(x1, y1), Point(x2, y2))
                rect.setFill('white')
                rect.draw(win)
            if(grid[column][row][0] == 3):      #Repaint wires
                rect = Rectangle(Point(x1, y1), Point(x2, y2))
                rect.setFill(colours[grid[column][row][1]])
                rect.draw(win)

def clearTrial(grid):
    global h, w, win, winsize, colours
    gsize = max(h,w)
    side = winsize / gsize
    color = cycle(colours)
    drawSquares('white')
    for row in range(h):
        y1 = row * side
        y2 = y1 + side
        for column in range(w):
            x1 = column * side
            x2 = x1 + side
            if(grid[column][row][0] == 0):      #Clear the FREE blocks
                rect = Rectangle(Point(x1, y1), Point(x2, y2))
                rect.setFill('white')
                rect.draw(win)
            if(grid[column][row][0] == 1):      #Repaint obstacles
                rect = Rectangle(Point(x1, y1), Point(x2, y2))
                rect.setFill('blue')
                rect.draw(win)


            
def click():
    global win
    win.getMouse()