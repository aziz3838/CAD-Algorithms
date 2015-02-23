'''
Created on Feb 21, 2015

@author: Abdulaziz Alghamdi
'''

import sys, getopt
from os import listdir, path
import time

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def main():
    x = np.linspace(0, 10)
    line, = plt.plot(x, np.sin(x), '--', linewidth=2)
    
    dashes = [10, 5, 100, 5] # 10 points on, 5 off, 100 on, 5 off
    line.set_dashes(dashes)
    
    plt.show()