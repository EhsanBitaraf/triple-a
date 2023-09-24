import pytest
import networkx as nx

@pytest.fixture
def cgraph():
    G = nx.complete_graph(100)
    return G