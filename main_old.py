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
    plot_features(M)

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

def plot_features(M):
    # plots the features in 2D space
    #M = mds(M)
    M = PCA(M)
    fig = plt.figure()
    colors = ["g"]*10 + ["r"]*10 + ["b"]*10 + ['y']*10 + ["m"]*10 + ["k"]*10 + ["c"]*10 + [ 0.3 ]*10 + [0.5]*10 + [0.8]*10
    #print(colors)
    ax = fig.add_subplot(111, projection='3d')    
    ax.scatter(M[:,0], M[:,1], M[:,2],marker='o', c=colors)
    '''
    ax = fig.add_subplot(111)
    ax.scatter(M[:,0],M[:,1], marker='o', c=colors)
    '''
    plt.show()


def mds(cloud):
    cloud -= np.mean(cloud,axis = 0,keepdims = True)
    #sklearn.preprocessing.normalize(cloud, copy = False)
    gram = cloud @ cloud.transpose()
    eigs,vectors = np.linalg.eig(gram)
    D = np.diag(eigs)
    reduced = vectors @ D
    return reduced

def PCA(M,n=3):
    #M -= np.mean(M,axis = 0,keepdims = True)
    U, s, Vt = np.linalg.svd(M)
    V = Vt.T
    S = np.diag(s)
    return np.dot(U[:, :n], S[:n, :n])

if __name__ == "__main__":
    redo = input("Do you wish to recompute all features ? (y/n) If no, features.txt we be used : ") == "y"
    if redo:
        compute_all_features()
    else:
        M = read_features()
        plot_features(M)
    
