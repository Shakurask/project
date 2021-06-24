import numpy as np
import igraph as ig



def get_timeline_matrix(timeline, window):
    matrix = []
    values = list(timeline.values())
    for i in range(0, len(timeline.items())-window):
        matrix.append(values[i:i+window])
    return np.matrix(matrix)

def get_x_house(trajectory_matrix, u_matrix, window):
    res = np.zeros((u_matrix.shape[1], trajectory_matrix.shape[1]))
    for i in range(0, window):
        u_vec=u_matrix[i]
        test = u_vec.transpose().dot(trajectory_matrix).reshape(trajectory_matrix.shape[1])
        xuy = u_vec.reshape((u_vec.shape[0],1)).dot(test)
        res += xuy
    return res;



def hankellize(mat):
    l_star = 0
    k_star = 0
    if mat.shape[0]>mat.shape[1]:
        l_star = mat.shape[1]
    else:
        l_star = mat.shape[0]

    if mat.shape[0]<mat.shape[1]:
        k_star = mat.shape[1]
    else:
        k_star = mat.shape[0]
    big_n=mat.shape[0]*mat.shape[1]-1
    g = [big_n]
    k = 0
    for k in range(0, big_n-1):
        res = 0
        sub_res=0
        if k>=0 and k<(l_star-1):
           for m in range(0, k+1):
               sub_res+=mat[m,k-m]
           g.append((1/(k+1))*sub_res)
       
        if (l_star-1)<=k and k<=k_star-1:
            for m in range(0, l_star):
               sub_res+=mat[m,k-m]
            g.append((1/l_star)*sub_res)
        if k_star< k and k<= big_n:
            for m in range(k-k_star, mat.shape[0]-k_star):
               sub_res+=mat[m,k-m]
            g.append((1/(big_n-k))*sub_res)
    return g;
