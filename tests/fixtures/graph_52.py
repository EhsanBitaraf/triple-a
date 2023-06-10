
import pytest
import networkx as nx


"""
This is a pytest fixture that sets up a graph object by reading a graphml file.
52 Article(s) 
979 Nodes & 1466 Edges
"""
@pytest.fixture
def graph52():
    # set up code goes here
    # G = nx.read_graphml('graph' / 'g52.graphml')
    G = nx.read_graphml('tests\\fixtures\\g52.graphml')
    yield G
    