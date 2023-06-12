from triplea.service.graph.analysis import (
    get_avg_shortest_path_length_per_node,
    get_clustering_coefficient_per_node,
)


def test_get_avg_shortest_path_length_per_node(graph52):
    s = get_avg_shortest_path_length_per_node(graph52)
    assert s[1] == 1


def test_get_clustering_coefficient_per_node(graph52):
    s = get_clustering_coefficient_per_node(graph52)
    assert  s[0] == 1

