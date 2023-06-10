from tests.fixtures.graph_52 import graph52
from triplea.service.graph.analysis import graph_diameter
from triplea.service.graph.analysis.neighbor_number import average_neighbor_number

def test_average_neighbor_number(graph52):
    assert average_neighbor_number(graph52) == 3.0353430353430353