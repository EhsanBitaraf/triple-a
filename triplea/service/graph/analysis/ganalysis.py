import networkx as nx

# import nxviz as nv??
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from netwulf import visualize
from networkx.classes.function import is_directed


def visualize_and_grouping(G):
    for k, v in G.nodes(data=True):
        v["group"] = v["Type"]
        del v["Type"]

    # Set node 'size' attributes
    for n, data in G.nodes(data=True):
        data["size"] = (3 * nx.degree(G, n)) + 2
        # data['size'] = np.random.random()
    visualize(G)


def sorted_degree_centrality(G) -> pd.Series:
    # NetworkX provides a function for us to calculate degree centrality conveniently:
    dcs = pd.Series(nx.degree_centrality(G))
    dcs = dcs.sort_values(ascending=False)
    return dcs


def sorted_average_neighbor_degree(G) -> pd.Series:
    dcs = pd.Series(nx.average_neighbor_degree(G))
    dcs = dcs.sort_values(ascending=False)
    return dcs


def average_neighbor_number(G) -> float:
    """
    For each node in the graph, count the number of neighbors and calculate average neighbor number for graph.

    :param G: a networkx graph
    :return: The average number of neighbors of a node in the graph.
    """
    H = G.to_undirected()
    i = 0
    sum_neighbors = 0
    for n in list(H.nodes(data=True)):
        i = i + 1
        node = n[0]
        iter = H.neighbors(node)
        num_neighbors = len(list(iter))
        sum_neighbors = sum_neighbors + num_neighbors

    return sum_neighbors / i


# def sorted_in_degree(G)->pd.Series:
#     # NetworkX provides a function for us to calculate degree centrality conveniently:
#     dcs = pd.Series(G.in_degree())
#     dcs = dcs.sort_values(ascending=False)
#     return dcs


def sorted_triangles(G) -> pd.Series:
    # NetworkX provides a function for us to calculate degree centrality conveniently:
    dcs = pd.Series(nx.triangles(G))
    dcs = dcs.sort_values(ascending=False)
    return dcs


def sorted_degree(G) -> pd.Series:
    # ?
    dcs = pd.Series(nx.degree(G))
    dcs = dcs.sort_values(ascending=False)
    return dcs


def sorted_betweenness_centrality(G):
    dcs = pd.Series(nx.betweenness_centrality(G))
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
    # plt.scatter(x, y)
    plt.plot(x, y)
    plt.show()


def get_top_keys(dictionary, top):
    items = dictionary.items()
    sort_items = dict(sorted(items, reverse=True, key=lambda item: item[1]))
    top = {k: sort_items[k] for k in list(sort_items)[:top]}
    return top


def info(G):
    if is_directed(G):
        print("Graph Type: Directed")
        print(f"SCC: {nx.number_strongly_connected_components(G)}")
        print(f"WCC: {nx.number_weakly_connected_components(G)}")
        print(f"Reciprocity : {nx.reciprocity(G)}")
    else:
        print("Graph Type: Undirected")
        # G.s_metric()
        diameter = nx.diameter(G)
        print(f"Graph Diameter : {diameter}")

    density = nx.density(G)
    transitivity = nx.transitivity(G)
    number_of_edges = nx.number_of_edges(G)
    number_of_nodes = nx.number_of_nodes(G)
    avg_deg = float(number_of_edges) / number_of_nodes
    try:
        dag_longest_path_length = nx.dag_longest_path_length(G)
    except Exception:
        # Graph contains a cycle or graph changed during iteration
        dag_longest_path_length = 'NaN'

    average_clustering = nx.average_clustering(G)
    degree_assortativity_coefficient = nx.degree_assortativity_coefficient(G)
    print(f"Graph Nodes: {number_of_nodes}")
    print(f"Graph Edges: {number_of_edges}")
    print(f"Graph Average Degree : {avg_deg}")
    print(f"Graph Density : {density}")
    print(f"Graph Transitivity : {transitivity}")
    print(f"Graph max path length : {dag_longest_path_length}")
    print(f"Graph Average Clustering Coefficient : {average_clustering}")
    print(
        f"Graph Degree Assortativity Coefficient : {degree_assortativity_coefficient}"
    )

    # bet_cen = nx.betweenness_centrality(G)
    # clo_cen = nx.closeness_centrality(G)
    # eig_cen = nx.eigenvector_centrality(G)
    # print(f'Graph Betweenness Centrality: {get_top_keys(bet_cen,1)}')
    # print(f'Graph Closeness Centrality: {get_top_keys(clo_cen,1)}')
    # print(f'Graph Eigenvector Centrality : {get_top_keys(eig_cen, 1)}')
