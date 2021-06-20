import igraph as ig
import matplotlib.pyplot as plt
import csv
import math
import colorsys
import random
import datetime
import numpy as np
from scipy.linalg import svd
from igraph import *

g = Graph(directed=True)

table = {}
vertices_count = 0
def read_vertices():
    with open("Cit-HepTh-dates.txt", "r") as f:
        print("reading csv")
        reader = csv.DictReader(f, delimiter=',')
    
        
        print("building graph")
    
        i=0
        for vert in reader:
            g.add_vertices(1);
            g.vs[i]["NodeId"]=vert["NodeId"]
            g.vs[i]["Date"]=vert["Date"]
            table[vert["NodeId"]] = i
            i+=1
        print("nodes: " + str(i));
        vertices_count=i
        
read_vertices()


def read_edges():
    with open("Cit-HepTh.txt", "r") as f2:
        print("reading graph edges")
        reader2 = csv.DictReader(f2, delimiter='\t')
        j = 0
        e = []
        for edge in reader2:
            if(edge["FromNodeId"] in table and edge["ToNodeId"] in table):
                e.append((table[edge["FromNodeId"]], table[edge["ToNodeId"]]));
            if j%1000==0:
                print(j)
            j = j+1;
    return e

e = read_edges();

print("building edges")
g.add_edges(e);


def clean_dataset(g):
    list_delete = []
    for v in g.vs:
        out_n = g.neighbors(v, mode="out")
        in_n = g.neighbors(v, mode="in")

        if len(list(set(out_n) & set(in_n)))>0:
            list_delete.append(v)
            continue
        if len(list(set(out_n))) + len(list(set(in_n)))<3:
               list_delete.append(v)
    

    g.delete_vertices(list_delete)
    list_delete.clear()

    for v in g.vs:
        out_n = g.neighbors(v, mode="out")
        in_n = g.neighbors(v, mode="in")
        if len(list(set(out_n))) + len(list(set(in_n)))<3:
               list_delete.append(v)

    g.delete_vertices(list_delete)
 
    g.delete_vertices(g.vs(_degree_lt=3))

clean_dataset(g)
vertices_count = len(list(g.vs))

def get_entropy(gr):
    probs = {}
    
    for v_degree in gr.vs.degree():
        if(v_degree in probs):
            probs[v_degree]=probs[v_degree]+1
        else:
           probs[v_degree]=1
    
    
    ent=0
    v_c = len(gr.vs)
    for cnt in probs.values():
        p=cnt/v_c
        ent+=p*math.log2(p)
    return  ent

def get_sub_entropy(gr):
    probs = {}
    
    for v_degree in gr.degree():
        if(v_degree in probs):
            probs[v_degree]=probs[v_degree]+1
        else:
           probs[v_degree]=1
    
    
    ent=0
    v_c = len(gr)
    for cnt in probs.values():
        p=cnt/v_c
        ent+=p*math.log2(p)
    return  ent


ent = get_entropy(g)


verts = list(g.vs)





out_n_list = {}
for v in verts:
    out_n_list[v] = g.neighbors(v, mode="all")

def get_timeline(sub_g):
    
    date_timeline = {}
    for j in range(1, 117):
        date_timeline[j]=0

    dates = sub_g.vs["Date"]
    dates = list(map(lambda x:datetime.datetime.strptime(x, '%Y-%m-%d'),dates))

    for date in dates:
        diff = int((date - datetime.datetime(1993, 1, 1)).days/30)
        date_timeline[diff] = date_timeline[diff] + 1
    c = 0
    for (m, count) in date_timeline.items():
        c+=count
        date_timeline[m] = c
    return date_timeline;
def plot_timeline(date_timeline):
    fig, ax = plt.subplots()

    ax.bar(date_timeline.keys(), date_timeline.values())

    ax.set_facecolor('seashell')
    fig.set_facecolor('floralwhite')
    fig.set_figwidth(12)    #  ширина Figure
    fig.set_figheight(6)    #  высота Figure

    plt.show()


timeline = get_timeline(g)

l = []

dendr = g.as_undirected().community_leading_eigenvector()
#dendr = g.community_edge_betweenness(20)
best_classes = []




def get_timeline_matrix(timeline, window):
    matrix = []
    values = list(timeline.values())
    for i in range(0, len(timeline.items())-window):
        matrix.append(values[i:i+window])
    return np.matrix(matrix)

def get_x_house(trajectory_matrix, u_matrix, window):
    res = np.zeros((u_matrix.shape[0], window))
    for i in range(0, window):
        u_vec=u_matrix[i]
        test = u_vec.dot(trajectory_matrix)
        res += u_vec.transpose().dot(test)
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
           for m in range(1, k+2):
               sub_res+=mat[k-m+2-1, m-1]
           g.append((1/(k+1))*sub_res)
       
        if (l_star-1)<=k and k<k_star:
            for m in range(1, l_star+1):
               sub_res+=mat[ k-m+2-1,m-1]
            g.append((1/l_star)*sub_res)
        if k_star<= k and k< big_n:
            for m in range(k-mat.shape[1]+2, mat.shape[0]-k_star+2):
               sub_res+=mat[k-m+2-1, m-1]
            g.append((1/(big_n-k))*sub_res)
    return g;



def get_child_timeline(cluster, timeline):
    child_timeline = get_timeline(cluster)
    for (m, c) in child_timeline.items():
        if timeline[m] != 0:
            child_timeline[m] = c#/timeline[m]
        else:
            child_timeline[m] = 0
    return  child_timeline

def get_nu_square(mat_u):
    sum = 0
    for i in range(0, 7):
        test = mat_u[i, mat_u.shape[1]-1]
        sum=sum+test*test
    return sum;

def det_vector(mat_u, nu_square):
    asdas = np.zeros((110,))

    for i in range(0, 110):
        ur=mat_u[i, 6-1]/(1-nu_square)
        asdas=asdas+mat_u[i].dot(ur)
    return asdas

def predict(timeline, a_vec, horizon):
    sum = 0
    predicated_timeline = []

    datas = []

    for i in range(0, 6):
        datas.append(timeline[len(timeline)-1-(6-i-1)])
    for h in range(0, horizon):
        for i in range(0, 6):
           comp = a_vec[0, i]
           sum = sum + datas[i+h] * comp
        datas.append(sum)
        predicated_timeline.append(sum)
    return predicated_timeline;

i = 0
for cluster in dendr.subgraphs():

    entropy = get_sub_entropy(cluster.vs)
    if entropy > -3.65 and len(list(cluster.vs)) > 8:
        print(entropy)
        best_classes.append(i)
        child_timeline = get_child_timeline(cluster, timeline)
        mat = get_timeline_matrix(child_timeline, 6)
        test = np.linalg.svd(mat)
        x_house = get_x_house(mat, test[0], 6)
        hank_x = hankellize(x_house)

        for x in hank_x:
            print(x)
        nu_square = get_nu_square(test[0])
        a_vec = det_vector(test[0], nu_square)
        ans = predict(child_timeline, a_vec, 6)
        plot_timeline(child_timeline)
    i = i+1

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

def save_graph_image():
    layout = g.layout("drl")
    plot(dendr,bbox=(8000, 8000), mark_groups = True, target="clusters.png")
    plot(g, layout=layout, bbox=(8000, 8000), margin=10, vertex_size = 8, target="graph2.png")
    return layout

layout = save_graph_image()


#fig, ax = plt.subplots()
#plot(g, layout=layout, target=ax)



