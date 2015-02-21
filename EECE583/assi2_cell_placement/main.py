'''
Created on Feb 21, 2015

@author: Abdulaziz Alghamdi
'''

import readfile
import placement
import sys, getopt

def main():
    
    blocklist, num_rows, num_cols = readfile.read('benchmarks/cm138a.txt')
    placement.initialize(blocklist, num_rows, num_cols)

main()
    