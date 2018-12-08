import sys
import itertools as it

# this file allows to compute filtrations from OFF files

def clean_line(line,t):
    line = line.strip(" \n").split(" ")
    while "" in line:
        line.remove("")
    for i in range(len(line)):
        line[i] = t(line[i])
    return line

def save_filtration(file_name):
    filtration = [] #value, dim, vertices
    edges_dic = {-1:0}

    with open('off_files/'+file_name,'r') as f:
        lines = f.readlines()
        # the first line holds no information, the second has the meta parameters
        line = clean_line(lines[1],int)
        n = int(line[0]) # number of 
        m = int(line[1]) # number of triangles
        assert(n+m+2 == len(lines)),str(n+m+2)+' '+str(len(lines))
        for k in range(2,n+2): # we add the vertices
            line = clean_line(lines[k],float)
            filtration.append([line[1],0,len(filtration)])
        for k in range(n+2,n+m+2): # we add the vertices
            line = clean_line(lines[k],int)
            line = line[1:]
            edges = it.combinations(line,2)
            for edge in edges:
                edge = list(edge)
                edge.sort()
                if tuple(edge) in edges_dic:
                    continue
                else:
                    edges_dic[tuple(edge)]=1
                value = max( filtration[edge[0]][0], filtration[edge[1]][0] )
                filtration.append([value,1,edge[0],edge[1]])
            value = max( filtration[line[0]][0], filtration[line[1]][0], filtration[line[2]][0] )
            filtration.append([value,2,line[0],line[1],line[2]])

    filtration.sort( key = lambda e : e[0:2] )

    output_name = file_name.split(".")[0]+".txt"
    with open('filtrations/'+output_name,'w') as f:
        for line in filtration:
            sline = ""
            for el in line:
                sline+= str(el)+ " "
            sline = sline[:-1]
            f.write(sline+"\n")

if __name__ == '__main__':
    try:
        file_number = int(sys.argv[1])
        if file_number<10:
            file_number = '00'+str(file_number)
        elif file_number<100:
            file_number = '0'+str(file_number)
        else:
            file_number = str(file_number)
    except (ValueError, IndexError):
        file_number = "001"
    file_name = 'tr_reg_'+str(file_number)+".off"
    save_filtration(file_name)


            

