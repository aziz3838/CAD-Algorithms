'''
Created on Jan 23, 2015

@author: Abdulaziz Alghamdi
'''


import drawing
import readfile
import path
import sys, getopt

def main():
    
    grid, pins = readfile.read()
    path.maze(grid, pins)
    drawing.click()
    

main()
    