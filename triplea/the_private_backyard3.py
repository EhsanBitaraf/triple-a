


from tests.fixtures.graph_52 import graph52_instance
from triplea.cli import export_graph

import triplea.cli as cli

from triplea.service.repository.import_file.triplea import import_triplea_json

from triplea.service.graph.analysis.ganalysis import get_avg_shortest_path_length_per_node, get_clustering_coefficient_per_node
import networkx as nx
if __name__ == "__main__":
    pass
    # import_triplea_json(r"C:\Users\Bitaraf\Desktop\ff\BibliometricAnalysis.json",True)
    # G = nx.star_graph(5)
    G = graph52_instance()
    # G = nx.read_graphml('tests\\fixtures\\g52.graphml')
    
    result = get_avg_shortest_path_length_per_node(G)
    print(result[0])


