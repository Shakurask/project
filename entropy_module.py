import math



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
