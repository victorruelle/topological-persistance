import numpy as np
import compute_barcodes
import extract_features
import filtration_from_off
import plot_barcode
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib


def compute_all_features():
    M = []
    for i in range(100):
        if i<10:
            i = '00'+str(i)
        elif i<100:
            i = '0'+str(i)
        else:
            i = str(i)
        filtration_from_off.save_filtration('tr_reg_'+i+'.off')
        compute_barcodes.save_barcode('tr_reg_'+i+'.txt')
        vector = extract_features.mapping('tr_reg_'+i+'.txt',2,10)
        M.append(vector)
        print("completed",i,"%")

    M = np.array(M)
    print("finished computing features")
    save_features(M)
    print("features saved")

def save_features(M):
    with open("features.txt",'w') as f:
        for line in M:
            t = ""
            for el in line:
                t += str(el)+" "
            t = t[:-1]+"\n"
            f.write(t)

def read_features():
    M = []
    with open("features2.txt",'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip("\n").split(" ")
            M.append([])
            for el in line:
                M[-1].append(float(el))
    return M

if __name__ == "__main__":
    redo = input("Do you wish to recompute all features ? (y/n) : ") == "y"
    if redo:
        compute_all_features()
    
