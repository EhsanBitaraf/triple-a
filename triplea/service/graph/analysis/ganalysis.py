import networkx as nx

# import nxviz as nv??
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from netwulf import visualize
# from networkx.classes.function import is_directed


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


def sorted_closeness_centrality(G):
    dcs = pd.Series(nx.closeness_centrality(G))
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


def get_avg_shortest_path_length_per_node(G):
    """
    Calculate the average shortest-path length for each node in the graph.

    Parameters:
    G (networkx.Graph): The input graph.

    Returns:
    pandas.Series: A series containing the average shortest-path length
    for each node, sorted in descending order.
    """

    # Calculate the average shortest-path length for each node
    avg_shortest_path_lengths = dict(nx.all_pairs_shortest_path_length(G))

    # Store the average shortest-path length for each node in a list of tuples
    ll = []
    for node in avg_shortest_path_lengths:
        avg_shortest_path_length = sum(avg_shortest_path_lengths[node].values()) / (
            len(G) - 1
        )
        ll.append((node, avg_shortest_path_length))

    # Convert the list of tuples to a pandas Series
    # and sort it in descending order
    dcs = pd.Series(dict(ll))
    dcs = dcs.sort_values(ascending=False)

    return dcs


def get_clustering_coefficient_per_node(G):
    # Calculate the clustering coefficient for each node
    s = {}
    for node in G.nodes():
        neighbors = list(G.neighbors(node))
        if len(neighbors) <= 1:
            # print(f"Node {node}: N/A")
            s[node] = None
        else:
            num_connected = 0
            for i in range(len(neighbors)):
                for j in range(i + 1, len(neighbors)):
                    if G.has_edge(neighbors[i], neighbors[j]):
                        num_connected += 1
            cc = num_connected / (len(neighbors) * (len(neighbors) - 1) / 2)
            # print(f"Node {node}: {cc}")
            s[node] = cc

    dcs = pd.Series(s)
    dcs = dcs.sort_values(ascending=False)

    return dcs
