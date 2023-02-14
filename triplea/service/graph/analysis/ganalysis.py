
import json
from triplea.schemas.article import Article
from triplea.schemas.node import Edge, Node
from triplea.service.export import generate_networkX
from triplea.service.persist import get_article_by_state
from triplea.service.click_logger import logger

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


def get_top_keys(dictionary, top):
    items = dictionary.items()
    sort_items = dict(sorted(items,reverse=True, key=lambda item: item[1]))
    top = {k: sort_items[k] for k in list(sort_items)[:top]}
    return top


from networkx.classes.function import is_directed

def info(G):
    if is_directed(G) :
        print('Graph Type: Directed')
        print (f'SCC: {nx.number_strongly_connected_components(G)}')
        print (f'WCC: {nx.number_weakly_connected_components(G)}')
        print (f'Reciprocity : {nx.reciprocity(G)}' )
    else:
        print('Graph Type: Undirected')
        # G.s_metric()

    density = nx.density(G)
    transitivity = nx.transitivity(G)
    number_of_edges = nx.number_of_edges(G)
    number_of_nodes = nx.number_of_nodes(G)
    avg_deg = float(number_of_edges) / number_of_nodes
    print(f'Graph Nodes: {number_of_nodes}')
    print(f'Graph Edges: {number_of_edges}')
    print(f'Graph Average Degree : {avg_deg}')
    print(f'Graph Density : {density}')
    print(f'Graph Transitivity : {transitivity}')

    
   
    # bet_cen = nx.betweenness_centrality(G)
    # clo_cen = nx.closeness_centrality(G)
    # eig_cen = nx.eigenvector_centrality(G)
    # print(f'Graph Betweenness Centrality: {get_top_keys(bet_cen,1)}')
    # print(f'Graph Closeness Centrality: {get_top_keys(clo_cen,1)}')
    # print(f'Graph Eigenvector Centrality : {get_top_keys(eig_cen, 1)}')

def generate_custom_graph():
    la = get_article_by_state(3)
    nodes = []
    edges = []
    MJ = []
    n = 0 
    for a in la:
        n = n + 1
        updated_article = Article(**a.copy())

        node_article = Node()
        node_article.Identifier = updated_article.PMID
        node_article.Name = updated_article.PMID
        node_article.Type = 'Article'
        nodes.append(node_article)

        if updated_article.NamedEntities is not None:
            for ner in updated_article.NamedEntities:
                node_entity = Node()
                node_entity.Identifier = ner.Entity
                node_entity.Name = ner.Entity
                if ner.Label=='MAJORTOPIC':
                    new_cluster_entity = ner.Entity.lower()

                    if new_cluster_entity.__contains__('registr'):new_cluster_entity = 'registry'
                    if new_cluster_entity.__contains__('data'):new_cluster_entity = 'data'
                    if new_cluster_entity.__contains__('record'):new_cluster_entity = 'record'
                    if new_cluster_entity.__contains__('screening'):new_cluster_entity = 'screening'
     

                    
                    node_entity.Identifier = new_cluster_entity
                    node_entity.Name = new_cluster_entity
                    MJ.append(new_cluster_entity)

                
                node_entity.Type = 'Entity'
                nodes.append(node_entity)

                edge_label = Edge()
                edge_label.SourceID = node_article.Identifier
                edge_label.DestinationID = node_entity.Identifier
                edge_label.Type = ner.Label
                edge_label.HashID =  str(hash(edge_label.SourceID + edge_label.DestinationID + edge_label.Type))
                edges.append(edge_label)




        logger.INFO(f'{n} article(s) read.')


    nodes_json= json.dumps(MJ, indent=4)
    with open("nodes.json", "w") as outfile:
        outfile.write(nodes_json)
    
    G = generate_networkX(nodes,edges)
    return G

def generate_custom_keyword_graph():
    la = get_article_by_state(3)
    nodes = []
    edges = []
    MJ = []
    n = 0 
    for a in la:
        n = n + 1
        updated_article = Article(**a.copy())

        node_article = Node()
        node_article.Identifier = updated_article.PMID
        node_article.Name = updated_article.PMID
        node_article.Type = 'Article'
        nodes.append(node_article)

        if updated_article.Keywords is not None:
            for k in updated_article.Keywords:
                node_entity = Node()
                node_entity.Identifier = k.Text
                node_entity.Name = k.Text
                node_entity.Type = 'Keyword'
                nodes.append(node_entity)

                MJ.append(node_entity.Name)

                edge_label = Edge()
                edge_label.SourceID = node_article.Identifier
                edge_label.DestinationID = node_entity.Identifier
                edge_label.Type = 'KEYWORD'
                edge_label.HashID =  str(hash(edge_label.SourceID + edge_label.DestinationID + edge_label.Type))
                edges.append(edge_label)

        logger.INFO(f'{n} article(s) read.')


    nodes_json= json.dumps(MJ, indent=4)
    with open("nodes.json", "w") as outfile:
        outfile.write(nodes_json)
    
    G = generate_networkX(nodes,edges)
    return G





if __name__ == '__main__':


    # G = generate_custom_graph()
    G = generate_custom_keyword_graph()
    # saving graph created above in graphml format
    nx.write_graphml(G, "NER.graphml")
    info(G)
    print(sorted_degree_centrality(G))
    visualize_and_grouping(G)


    # G = export_networkX(graph_type='undirected')
    # G = export_networkX()

    #region lab

    # print(len(G.edges))
    # print(nx.number_of_nodes(G))
    # print(nx.number_of_edges(G))

    # print(nx.info(G))
    # print(nx.triangles(G, 6))

    # print(sorted(nx.pagerank_numpy(G[0],
    #     weight=None).items(),
    #     key=lambda x:x[1], reverse=True)[0:10])

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
    # H = nx.Graph(((u, v, e) for u,v,e in G.edges(data=True) if e['Type'] == 'KEYWORD'))
    # visualize(H)
    # print(nx.number_of_nodes(H))
    # print(nx.number_of_edges(H))
    # print(sorted_betweenness_centrality(H))
    # print(H.out_degree('Electronic Health Records'))
    # print(H.in_degree('Electronic Health Records'))
    # nx.draw_circular(H, with_labels=True)
    # nx.draw_shell(H)
    # plt.savefig("path.png")
    # from networkx.algorithms.smetric import s_metric
    # print(s_metric(H))
    
    # print(nx.diameter(H))
 

    # G = H
    # info(G) 
    # print(nx.is_connected(G))

    # # Next, use nx.connected_components to get the list of components,
    # # then use the max() command to find the largest one:
    # components = nx.connected_components(G)
    # largest_component = max(components, key=len)

    # # Create a "subgraph" of just the largest component
    # # Then calculate the diameter of the subgraph, just like you did with density.
    # #

    # subgraph = G.subgraph(largest_component)
    # diameter = nx.diameter(subgraph)
    # print("Network diameter of largest component:", diameter)
    # # print(nx.s_metric(G))
    # info(subgraph)

    # Connected components are sorted in descending order of their size
    # cam_net_components = nx.connected_component_subgraphs(G)
    # connected_component_subgraphs() has been removed from version 2.4.
    # G = G.to_undirected()
    # connected_component_subgraphs = (G.subgraph(c) for c in nx.connected_components(G))
    # largest_subgraph = max(connected_component_subgraphs, key=len)
    # print('--------------------')
    # info(largest_subgraph)
    # cam_net_mc = largest_subgraph[0]
    # # Betweenness centrality
    # bet_cen = nx.betweenness_centrality(cam_net_mc)
    # # Closeness centrality
    # clo_cen = nx.closeness_centrality(cam_net_mc)
    # # Eigenvector centrality
    # eig_cen = nx.eigenvector_centrality(cam_net_mc)


    # Modularity
    # Modularity is a metric for understanding how well a network can be partitioned into separate clusters. The general rule is, the greater the modularity, the higher the number of highly connected groups connected by sparse edges.
    # G = nx.complete_graph(100)
    # G = G.to_undirected()
    # info(G) 
    # import networkx.algorithms.community as nx_comm
    # print(nx_comm.modularity(G, G.nodes()))

    
    #endregion










