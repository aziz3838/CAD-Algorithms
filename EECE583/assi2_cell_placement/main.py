'''
Created on Feb 21, 2015

@author: Abdulaziz Alghamdi
'''

from readfile import read
from placement import *
import sys, getopt

def main():
    
    blocklist, num_rows, num_cols = read('benchmarks/cm138a.txt')
    initialize(blocklist, num_rows, num_cols)

main()
    