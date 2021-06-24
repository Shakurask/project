import igraph as ig
import math
import csv

def read_vertices(g,table,vertices_count):
    
    with open("Cit-HepTh-dates.txt", "r") as f:
       
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


def read_edges(table):
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