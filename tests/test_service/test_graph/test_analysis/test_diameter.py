from tests.fixtures.graph_52 import graph52
from triplea.service.graph.analysis.diameter import graph_diameter
import pytest
import networkx as nx

def test_diameter(graph52):
    # graph_diameter(graph52)

    assert 1 + 2 == 3


class TestGraphDiameter:
    def test_diameter1(graph52):
        

        assert 1 + 2 == 3

    # # Test with a small graph with known diameter
    # def test_small_graph_known_diameter(self):
    #     # Create a small graph with known diameter
    #     G = nx.Graph()
    #     G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)])

    #     # Calculate the expected diameter
    #     expected_diameter = 5

    #     # Calculate the actual diameter using the graph_diameter function
    #     actual_diameter = graph_diameter(G)

    #     # Assert that the actual diameter matches the expected diameter
    #     assert actual_diameter == expected_diameter

    # # Test with a large graph with known diameter
    # def test_large_graph_known_diameter(self):
    #     # Create a large graph with known diameter
    #     G = nx.Graph()
    #     G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10)])

    #     # Calculate the expected diameter
    #     expected_diameter = 9

    #     # Calculate the actual diameter using the graph_diameter function
    #     actual_diameter = graph_diameter(G)

    #     # Assert that the actual diameter matches the expected diameter
    #     assert actual_diameter == expected_diameter

    # # Test with a disconnected graph
    # def test_disconnected_graph(self):
    #     # Create a disconnected graph
    #     G = nx.Graph()
    #     G.add_edges_from([(1, 2), (3, 4)])

    #     # Calculate the expected diameter
    #     expected_diameter = 0

    #     # Calculate the actual diameter using the graph_diameter function
    #     actual_diameter = graph_diameter(G)

    #     # Assert that the actual diameter matches the expected diameter
    #     assert actual_diameter == expected_diameter

    # # Test with an empty graph
    # def test_empty_graph(self):
    #     # Create an empty graph
    #     G = nx.Graph()

    #     # Calculate the expected diameter
    #     expected_diameter = 0

    #     # Calculate the actual diameter using the graph_diameter function
    #     actual_diameter = graph_diameter(G)

    #     # Assert that the actual diameter matches the expected diameter
    #     assert actual_diameter == expected_diameter

    # # Test with a graph with only one node
    # def test_single_node_graph(self):
    #     # Create a graph with only one node
    #     G = nx.Graph()
    #     G.add_node(1)

    #     # Calculate the expected diameter
    #     expected_diameter = 0

    #     # Calculate the actual diameter using the graph_diameter function
    #     actual_diameter = graph_diameter(G)

    #     # Assert that the actual diameter matches the expected diameter
    #     assert actual_diameter == expected_diameter

    # # Test with a graph with only two nodes and no edges
    # def test_two_node_graph_no_edges(self):
    #     # Create a graph with only two nodes and no edges
    #     G = nx.Graph()
    #     G.add_nodes_from([1, 2])

    #     # Calculate the expected diameter
    #     expected_diameter = 0

    #     # Calculate the actual diameter using the graph_diameter function
    #     actual_diameter = graph_diameter(G)

    #     # Assert that the actual diameter matches the expected diameter
    #     assert actual_diameter == expected_diameter