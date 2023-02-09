from triplea.service.export import export_networkX
import networkx as nx
import nxviz as nv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from netwulf import visualize

def visualize_and_grouping(G):
    for k, v in G.nodes(data=True):
        v['group'] = v['Type']; del v['Type']

    # Set node 'size' attributes
    for n, data in G.nodes(data=True):
        data['size'] = (3 * nx.degree(G,n)) + 2
        # data['size'] = np.random.random()
    visualize(G)

def sorted_degree_centrality(G)->pd.Series:
    # NetworkX provides a function for us to calculate degree centrality conveniently:
    dcs = pd.Series(nx.degree_centrality(G))
    dcs = dcs.sort_values(ascending=False)
    return dcs

def sorted_degree(G)->pd.Series:
    # ?
    dcs = pd.Series(nx.degree(G))
    dcs = dcs.sort_values(ascending=False)
    return dcs

def sorted_betweenness_centrality(G):
    dcs = pd.Series(nx.betweenness_centrality(G))
    dcs = dcs.sort_values(ascending=False)
    return dcs

def sorted_triangles(G):
    dcs = pd.Series(nx.triangles(G))
    dcs = dcs.sort_values(ascending=False)
    return dcs

def sorted_clustering(G):
    dcs = pd.Series(nx.clustering(G))
    dcs = dcs.sort_values(ascending=False)
    return dcs

def filter_graph(G, minimum_num_trips):
    """
    Filter the graph such that
    only edges that have minimum_num_trips or more
    are present.
    """
    G_filtered = G.copy()
    for u, v, d in G.edges(data=True):
        if d["num_trips"] < minimum_num_trips:
            G_filtered.remove_edge(u, v)
    return 

def ecdf(data):
    return np.sort(data), np.arange(1, len(data) + 1) / len(data)


def show_degree_distribution(G):
    x, y = ecdf(pd.Series(dict(nx.degree(G))))
    plt.scatter(x, y)
    plt.show()

if __name__ == '__main__':
    # G = export_networkX(graph_type='undirected')
    G = export_networkX()

    # print(len(G.edges))
    print(nx.number_of_nodes(G))
    print(nx.number_of_edges(G))

    # print(sorted(nx.pagerank_numpy(G[0],
    #     weight=None).items(),
    #     key=lambda x:x[1], reverse=True)[0:10])

    # print(nx.info(G))
    # print(nx.triangles(G, 6))

    # print(G.edges.values())
    # list(G.edges(data=True))[0:5]
    # print(list(G.nodes(data=True))[0:5])
    # for e in list(G.edges):
    #     print(e)

    # subgraph_view()

    # G_filtered = filter_graph(G, 50)
    # c = nv.geo(G_filtered, node_color_by="dpcapacity")


    # c = nv.geo(G)


    # import matplotlib.pyplot as plt

    # er = nx.erdos_renyi_graph(30, 0.3)
    # print(type(G))
    # nx.draw(G)
    # nx.draw_networkx_edge_labels(G)
    # nx.draw_spectral(G,with_labels=True,node_size=2)
    # nx.draw_kamada_kawai(G)
    # plt.show()

    

    # from nxviz.plots import ArcPlot
    # from nxviz.plots import MatrixPlot
    # from nxviz.plots import CircosPlot
    # m = MatrixPlot(G)
    # m.draw()
    # plt.show()

    # fig, ax = plt.subplots(figsize=(7, 7))
    # nv.circos(G)
    # nv.MatrixPlot(G)
    # nv.ArcPlot(G)
    # plt.show()

    # d = G.neighbors('Hospital Information Systems')
    # d = G.neighbors('33430992')
    # print(d)

    # export_networkx_to_gpickle('test.pkl') # has error
    # ps = sorted_degree_centrality(G)
    # ps = sorted_betweenness_centrality(G)
    # ps = sorted_triangles(G)
    # ps = sorted_clustering(G)
    # ps = sorted_degree(G)
    # print(ps)
    
    # print(nx.graph_number_of_cliques(G))
    # print(nx.triangles(G,'36694161'))
    # print(nx.clustering(G,'36694161'))
    # print(nx.communicability(G))
    # print(nx.degree(G,'treatment outcome'))
    # G = nx.complete_graph(100)
    # G = nx.binomial_tree(3)
    # print(nx.density(G))


    # subG = nx.subgraph(G, ['33430992','36694161'])
    # print(len(subG.nodes))
    # print(len(subG.edges))

    # def filter_node(n1):
    #     if len(n1) == 6 :
    #         return n1
    #     # return n1 != 5
    # view = nx.subgraph_view(G, filter_node=filter_node)
    # print(len(view.nodes))
    # print(len(view.edges))
    # print(view.nodes())

    ## Query Graph

    # selected_nodes_keyword = [n for n,v in G.nodes(data=True) if v['Type'] == 'Keyword']
    # selected_nodes_Article = [n for n,v in G.nodes(data=True) if v['Type'] == 'Article']
    # selected_nodes_keyword.extend(selected_nodes_Article)
    # H = G.subgraph(selected_nodes_keyword)
    # nx.draw(H)
    # plt.show()

    # selected_edges = [(u,v) for u,v,e in G.edges(data=True) if e['Type'] == 'AUTHOR_OF']
    # H = G.subgraph(selected_edges)

    

    # print(nx.number_of_nodes(H))
    # print(nx.number_of_edges(H))
    # print(sorted_degree_centrality(H))
    # print(nx.density(H))
    # print(nx.degree(G,'Electronic Health Records'))

    
    # d = G.neighbors('31113484')
    # for n in d:
    #     # print(type(n))
    #     print(n)
    # print(d)


    # selected_edges = [(u,v,e) for u,v,e in G.edges(data=True) if v == '31113484']
    # H = nx.Graph(selected_edges)
    H = nx.Graph(((u, v, e) for u,v,e in G.edges(data=True) if e['Type'] == 'KEYWORD'))
    visualize(H)









