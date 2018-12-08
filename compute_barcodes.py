from numpy import inf
import numpy as np
import sys
from time import time
from random import random

class Simplex:

    def __init__(self,val,dim,vert, index=0):
        self.val = float(val)
        self.dim = int(dim)
        self.vert = [int(v) for v in vert]
        self.vert.sort()

    def show(self):
        print("val :",self.val," dim :",self.dim," vert :",self.vert)

def load_filtration(file_name):
    with open("filtrations/"+file_name,"r") as loaded_file:
        lines = loaded_file.readlines()
        simpl_complex = []
        for line in lines:
            line = line.strip("\n").split(" ")
            simpl_complex.append(Simplex(line[0],line[1],line[2:]))
        simpl_complex.sort(key = lambda simplex : [simplex.val,simplex.dim]+simplex.vert)
    return simpl_complex

def fast_boundary_matrix(simpl_complex):
    hmap = {}
    for i in range(len(simpl_complex)):
        s = simpl_complex[i]
        hmap[str(s.vert)] = i
    return [ fast_boundary_indices(simplex,hmap) for simplex in simpl_complex ]

def fast_boundary_indices(simplex,hmap):
    verts = [ simplex.vert[:i] + simplex.vert[i+1:] for i in range(len(simplex.vert))]
    indices = []
    for i in range(len(verts)):
        h = str(verts[i])
        if not(h in hmap):
            continue
        indices.append(hmap[h])
    indices.sort()
    return indices

def reduction(boundary_matrix):
    pivots = {}
    null_columns = []
    for j in range(len(boundary_matrix)):

        #checking if null column
        if len(boundary_matrix[j])==0:
            null_columns.append(j)
            continue
        candidate_pivot = boundary_matrix[j][-1]
        zeroed = False

        # GAUSSIAN PIVOT IN O(n^2)
        while candidate_pivot in pivots: # O(1) for call to keys
            new_column = []
            j_old = pivots[candidate_pivot]
            i,i_old = len(boundary_matrix[j])-1,len(boundary_matrix[j_old])-1
            while i>=0 and i_old>=0: # O(len(1)+len(2))
                if boundary_matrix[j][i] == boundary_matrix[j_old][i_old]:
                    i -= 1
                    i_old -= 1
                else:
                    new_column.append(max(boundary_matrix[j][i],boundary_matrix[j_old][i_old]))
                    i_old, i = (i_old-1,i) if boundary_matrix[j][i]<boundary_matrix[j_old][i_old] else (i_old,i-1)

            if i_old < 0: #comparaison finished, must copy all values remaining from other column
                new_column += boundary_matrix[j][:i+1]
            elif i < 0:
                new_column += boundary_matrix[j_old][:i_old+1]
                
            new_column.sort()
            boundary_matrix[j] = new_column
            if boundary_matrix[j]==[]:
                zeroed = True
                break
            candidate_pivot = boundary_matrix[j][-1]

        # COLUMN GENERATES A PIVOT OR IS NULLED
        if zeroed:
            null_columns.append(j)
        else:
            pivots[candidate_pivot] = j

    # NULLED COLUMNS MAY YIELD INFINITE SETS
    null_columns = [ j for j in null_columns if not(j in pivots)]
    for j in null_columns:
        pivots[j]=-1 # -1 represents infinity

    # EXTRA COMPUTING JUST TO GET SORTED OUTPUT
    pivots_list = [ (i,pivots[i]) for i in pivots ]
    pivots_list.sort()
    
    return pivots_list


compute_intervals = lambda pivots,simpl_complex: [ (simpl_complex[i].dim,simpl_complex[i].val,(inf if j==-1 else simpl_complex[j].val) ) for i,j in pivots ]

def print_bmatrix(bmatrix):
    M = np.matrix(np.zeros((len(bmatrix),len(bmatrix))))
    for j in range(len(bmatrix)):
        for i in bmatrix[j]:
            M[i,j] = 1 
    print(M)

def print_filtration(filtration):
    output = ''
    for s in filtration:
        output += str(s.vert)+"; "
    print(output[:-2])

def save_barcode(name):
    loaded_filtration = load_filtration(name)
    bmatrix = fast_boundary_matrix(loaded_filtration)
    pivots = reduction(bmatrix)
    res = compute_intervals(pivots,loaded_filtration)
    with open("bar_codes/"+name,'w') as out_file:
        for r in res:
            if r[2]-r[1] == 0:
                continue
            out_file.write(str(r[0])+","+str(r[1])+","+str(r[2])+"\n")

if __name__ == "__main__":
    print('running...')
    start = time()
    initial_start = start
    filtration_name = "input.csv" if len(sys.argv)==1 else sys.argv[1]
    print("filtration used:",filtration_name)
    loaded_filtration = load_filtration(filtration_name)
    #print_filtration(loaded_filtration)    
    print('filtration loaded in',time()-start)
    start = time()
    bmatrix = fast_boundary_matrix(loaded_filtration)
    #print_bmatrix(bmatrix)
    print("boundary matrix computed in",time()-start)
    start = time()
    pivots = reduction(bmatrix)
    print("pivots computed in",time()-start)
    start = time()
    res = compute_intervals(pivots,loaded_filtration)
    print('intervals computed in',time()-start)
    start = time()
    output_name = filtration_name.split(".")[0]+".txt" if len(sys.argv)<3 else sys.argv[2]
    print("writing result to","bar_codes/"+str(output_name))
    with open("bar_codes/"+output_name,"w") as out_file:
        for r in res:
            if r[2]-r[1] == 0:
                continue
            out_file.write(str(r[0])+","+str(r[1])+","+str(r[2])+"\n")
    print('results written to output file in',time()-start)
    print('total time',time()-initial_start)
