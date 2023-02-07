import networkx as nx
from triplea.schemas.node import Edge, Node

from triplea.service.persist import get_all_edges, get_all_nodes

def export_networkX():
    G = nx.DiGraph()

    nodes = get_all_nodes()
    for n in nodes:
        node = Node(**n.copy()) 
        G.add_node(node.Identifier , Type = node.Type)

    edges = get_all_edges()
    for e in edges:
        edge = Edge(**e.copy()) 
        G.add_edge(edge.SourceID , edge.DestinationID , Type = edge.Type)

    return G

def export_gexf():
    G = export_networkX()
    # saving graph created above in gexf format
    nx.write_gexf(G, "geeksforgeeks.gexf")

        



if __name__ == '__main__':
    # export_networkX()
    export_gexf()