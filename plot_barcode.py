import matplotlib.pyplot as plt
import numpy as np
import sys

def read_barcode(file_name):
    with open("bar_codes/"+file_name,'r') as f:
        lines = f.readlines()
        intervals = []
        for line in lines:
            line = line.strip().split(",")
            interval = [int(line[0]),float(line[1]),-1 if line[2]=="inf" else float(line[2])]
            intervals.append(interval)
    return intervals


def print_bar_code(file_name):
    intervals = read_barcode(file_name)
    long_intervals = [interval for interval in intervals if interval[2]==-1 or interval[2]-interval[1]>0.1]
    max_val = max( long_intervals, key = lambda interval : interval[2] )[2]
    long_intervals.sort(key = lambda interval : interval[0])
    level,offset = 0,0
    for i in range(len(long_intervals)):
        interval = long_intervals[i]
        new_level = interval[0]
        offset += (new_level - level)*3
        if interval[-1]>0:                
            plt.plot([interval[1],interval[2]],[-i-offset,-i-offset],color = colors[interval[0]%len(colors)])
        else:
            plt.plot([interval[1],max_val*2.9],[-i-offset,-i-offset],color = colors[interval[0]%len(colors)], linestyle ="--")
        level = new_level
    plt.title("barcode of "+str(file_name.split('.')[0])+"\n a dashed line represents an infinite segment")
    plt.xlim(-1,max_val*3)
    plt.ylabel("")
    plt.yticks([])
    plt.show()

colors = ['b', 'g', 'r', 'c', 'm', 'y']

if __name__ == '__main__':
    try:
        print_bar_code(sys.argv[1])
    except IndexError:
        print('please enter a filename')
