import networkx as nx


def graph_diameter(G):
    """
    This function calculates the diameter of a network graph using the eccentricity
    of each node.

    :param G: a networkx graph object representing a network
    :return: the diameter of the input graph G.
    """
    # calculate eccentricity of each node
    eccentricities = nx.eccentricity(G)

    # calculate network diameter
    diameter = nx.diameter(G, eccentricity=eccentricities)

    return diameter
