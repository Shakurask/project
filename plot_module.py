










def save_graph_image():
    layout = g.layout("drl")
    plot(dendr,bbox=(8000, 8000), mark_groups = True, target="clusters.png")
    plot(g, layout=layout, bbox=(8000, 8000), margin=10, vertex_size = 8, target="graph2.png")
    return layout