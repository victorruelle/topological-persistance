from plot_barcode import read_barcode
import numpy as np
import sys

def mapping(filtration_name,d,n):
    # filtration_name should include the extension 
    # d: maximum desired homological dimension
    # n : maximum desired number of barcode intervals
    # we ignore the infinite intervals : since we take the distance function there will always be only one 0-D infinite interval
    intervals = read_barcode(filtration_name)
    finite_intervals = [ i for i in intervals if i[2]>0 ]
    
    vector = []
    for dimension in range(d+1):
        finite_intervals_d = [ i for i in finite_intervals if i[0]==dimension ]

        # first n values
        interval_lengths = [ i[2]-i[1] for i in finite_intervals_d ] + [0]*n
        interval_lengths.sort(reverse=True)
        interval_lengths = interval_lengths[:n]
        
        # next n(n-1)/2 values
        highest_entries = [0]*(int(n*(n-1)/2))

        for i in range(len(finite_intervals_d)):
            x = finite_intervals_d[i][1:]
            for j in range(i+1,len(finite_intervals_d)):
                y = finite_intervals_d[j][1:]
                #d = min( (-x[0]+x[1])/2,(-y[0]+y[1])/2, np.sqrt( np.square(y[1]-x[1])+np.square(y[0]-x[0]) ) )
                d = min( (-x[0]+x[1])/2,(-y[0]+y[1])/2, max( abs(y[1]-x[1]),abs(y[0]-x[0]) ) )
                if highest_entries[-1]<d:
                    highest_entries.append(d)
                    highest_entries.sort(reverse=True)
                    highest_entries = highest_entries[:-1]

        vector += interval_lengths + highest_entries
    return vector



if __name__ == '__main__':
    try:
        print(mapping(sys.argv[1],2,10))
    except IndexError:
        print('please enter a filename')