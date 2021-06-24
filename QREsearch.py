import igraph as ig
import matplotlib.pyplot as plt
import csv
import math
import colorsys
import random
import datetime
import numpy as np
import scipy
from scipy.linalg import svd
from igraph import *
from graph_module import *
from timeline_module import *
from entropy_module import *
from SVD_module import *
from plot_module import *
from predict_module import *


window = 12
predict_for = 3
print("reading csv")
g = Graph(directed=True)

table = {}
vertices_count = 0
   
read_vertices(g,table,vertices_count)

e = read_edges(table);

print("building edges")
g.add_edges(e);

clean_dataset(g)
vertices_count = len(list(g.vs))

ent = get_entropy(g)

verts = list(g.vs)

out_n_list = {}
for v in verts:
    out_n_list[v] = g.neighbors(v, mode="all")

timeline = get_timeline(g)
l = []
dendr = g.as_undirected().community_leading_eigenvector()
#dendr = g.community_edge_betweenness(20)
best_classes = []



def main(dendr,best_classes,timeline):
    i = 0
    for cluster in dendr.subgraphs():
    
        entropy = get_sub_entropy(cluster.vs)
        if entropy > -3.65 and len(list(cluster.vs)) > 8:
            print(entropy)
            best_classes.append(i)
            child_timeline = get_child_timeline(cluster, timeline)
            trajectory_matrix = get_timeline_matrix(child_timeline, window)
            екфо_укфо = trajectory_matrix.transpose().dot(trajectory_matrix)
            test = scipy.linalg.svd(trajectory_matrix)#
            test2 = scipy.linalg.orth(trajectory_matrix)
            u_mat = np.zeros((window,test[0].shape[1]))
            for j in range (0,window):
                u_mat[j] = test[0][j]
            x_house = get_x_house(trajectory_matrix, u_mat, window)
            hank_x = hankellize(x_house)
            
            for x in hank_x:
                print(x)
            nu_square = get_nu_square(u_mat,window-3)
            a_vec = det_vector(u_mat, nu_square,window)
            #a_vec = a_vec*(1/trajectory_matrix.shape[1])
            predict(child_timeline, a_vec,predict_for,window-3)
            plot_timeline(child_timeline)
            #plt.plot(ans)
        i = i+1

main(dendr,best_classes,timeline)

print("done")

print(ent)
delete_vertices = []
membership = dendr.membership
verts = dendr.graph.vs
for v in verts:
    if(membership[v.index] in best_classes):
        delete_vertices.append(v)
    else:
        print(v["NodeId"])
        print(membership[v.index])


g.delete_vertices(delete_vertices)
print("creating image")

g.write_gml("gml.gml")

#layout = save_graph_image()


#fig, ax = plt.subplots()
#plot(g, layout=layout, target=ax)



