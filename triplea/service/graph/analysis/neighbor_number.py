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
