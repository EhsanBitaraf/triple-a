import json
from typing import Optional
import networkx as nx
from triplea.schemas.node import Edge, Node

from triplea.service.persist import get_all_edges, get_all_nodes

def _check_graph():
    nodes = get_all_nodes()
    data_nodes = []
    for n in nodes:
        node = Node(**n.copy()) 
        data_nodes.append(node.Identifier)

    edges = get_all_edges()
    n = 0
    for e in edges:
       
        edge = Edge(**e.copy())  

        if edge.SourceID in data_nodes:  
            pass
        else:
            n = n + 1
            print(f'{n} | SourceID "{edge.SourceID}" Not Exist. ')

        if edge.DestinationID in data_nodes:  
            pass
        else:
            n = n + 1
            print(f'{n} | DestinationID "{edge.DestinationID}" Not Exist. in Type : {edge.Type} & SourceID =  "{edge.SourceID}"')

def export_graphjson()->dict:

    data = {}
    data['comment'] = 'This file generate autommaticlly by TripleA'
    nodes = get_all_nodes()
    data_nodes = []
    for n in nodes:
        node = Node(**n.copy()) 
        data_n = {}
        data_n['caption'] = node.Name
        data_n['type'] = node.Type
        data_n['id'] = node.Identifier
        data_nodes.append(data_n)

    edges = get_all_edges()
    data_edges = []
    for e in edges:
        edge = Edge(**e.copy()) 
        data_e = {}
        data_e['source'] = edge.SourceID
        data_e['target'] = edge.DestinationID
        data_e['caption'] = edge.Type
        data_edges.append(data_e)

    data['nodes'] = data_nodes
    data['edges'] = data_edges
    return data

def export_networkX(graph_type: Optional[str] = 'directed' ):
    """
    It takes a list of nodes and edges from a database and creates a networkX graph object
    :return: A networkx graph object
    """
    if graph_type == 'undirected':
        G = nx.Graph()
    elif graph_type == 'directed':
        G = nx.DiGraph()
    else:
        raise NotImplementedError

    nodes = get_all_nodes()
    for n in nodes:
        node = Node(**n.copy()) 
        G.add_node(node.Identifier , Type = node.Type, Name = node.Name)

    edges = get_all_edges()
    for e in edges:
        edge = Edge(**e.copy()) 
        G.add_edge(edge.SourceID , edge.DestinationID , Type = edge.Type)

    return G

def generate_networkX(nodes : list[Node] , edges : list[Edge], graph_type: Optional[str] = 'directed' ):
    if graph_type == 'undirected':
        G = nx.Graph()
    elif graph_type == 'directed':
        G = nx.DiGraph()
    else:
        raise NotImplementedError

    # nodes = get_all_nodes()
    for node in nodes:
        # node = Node(**n.copy()) 
        G.add_node(node.Identifier , Type = node.Type, Name = node.Name)

    # edges = get_all_edges()
    for edge in edges:
        # edge = Edge(**e.copy()) 
        G.add_edge(edge.SourceID , edge.DestinationID , Type = edge.Type)

    return G

def export_networkx_to_gpickle(filename:str):
    G = export_networkX()
    nx.write_gpickle(G, filename)
    # And just to show that it can be loaded back into memory:
    # G_loaded = nx.read_gpickle("/tmp/divvy.pkl")

def export_gexf(filename:str):
    """
    It creates a networkX graph object, and then saves it in the gexf format
    """
    G = export_networkX()
    # saving graph created above in gexf format
    nx.write_gexf(G, filename +  ".gexf")

def export_graphml(filename:str):
    G = export_networkX()
    # saving graph created above in graphml format
    nx.write_graphml(G, filename + ".graphml")


from triplea.config.settings import ROOT
import pandas as pd
# from nams.solutions.hubs import ecdf_degree
if __name__ == '__main__':
    # export_networkX()
    # export_gexf('ehr')
    # export_graphml('ehr')

    # # check integrity of graph
    # _check_graph()

    # print(ROOT.parent / 'visualization' / 'alchemy' / 'data.json')
    # data = export_graphjson()
    # data= json.dumps(data, indent=4)
    # with open(ROOT.parent / 'visualization' / 'alchemy' / 'data.json', "w") as outfile:
    #     outfile.write(data)

    G = export_networkX()



