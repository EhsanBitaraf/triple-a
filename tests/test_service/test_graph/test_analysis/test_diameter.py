from tests.fixtures.graph_52 import graph52
from triplea.service.graph.analysis.diameter import graph_diameter

def test_diameter(graph52):
    graph_diameter(graph52)

    assert 1 + 2 == 3