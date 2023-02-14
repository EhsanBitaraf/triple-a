import json
from typing import Optional
import networkx as nx
from triplea.schemas.node import Edge, Node
import triplea.service.repository.persist as persist

def _check_graph():
    nodes = persist.get_all_nodes()
    data_nodes = []
    for n in nodes:
        node = Node(**n.copy()) 
        data_nodes.append(node.Identifier)

    edges = persist.get_all_edges()
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

def export_graphjson_from_arepo()->dict:
    """
    It takes all the nodes and edges from the article repository and converts them into a format that can be used
    by the graph visualization library
    :return: A dictionary with two keys: nodes and edges.
    """
    data = {}
    data['comment'] = 'This file generate autommaticlly by TripleA'
    nodes = persist.get_all_nodes()
    data_nodes = []
    for n in nodes:
        node = Node(**n.copy()) 
        data_n = {}
        data_n['caption'] = node.Name
        data_n['type'] = node.Type
        data_n['id'] = node.Identifier
        data_nodes.append(data_n)

    edges = persist.get_all_edges()
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

def export_networkX_from_arepo(graph_type: Optional[str] = 'directed' ):
    """
    It takes a list of nodes and edges from the article repository and creates a networkX graph object
    :return: A networkx graph object
    """
    if graph_type == 'undirected':
        G = nx.Graph()
    elif graph_type == 'directed':
        G = nx.DiGraph()
    else:
        raise NotImplementedError

    nodes = persist.get_all_nodes()
    for n in nodes:
        node = Node(**n.copy()) 
        G.add_node(node.Identifier , Type = node.Type, Name = node.Name)

    edges = persist.get_all_edges()
    for e in edges:
        edge = Edge(**e.copy()) 
        G.add_edge(edge.SourceID , edge.DestinationID , Type = edge.Type)

    return G

def export_gpickle_from_arepo(filename:str):
    """
    It read article repository and extract node & edge from it, and then saves it in the [pickle format](https://docs.python.org/3/library/pickle.html).
    Pickles are a serialized byte stream of a Python object.
    
    :param filename: the name of the file to write to
    :type filename: str
    """
    G = export_networkX_from_arepo()
    nx.write_gpickle(G, filename)
    # And just to show that it can be loaded back into memory:
    # G_loaded = nx.read_gpickle("/tmp/divvy.pkl")

def export_gexf_from_arepo(filename:str):
    """
    It read article repository and extract node & edge from it, and then saves it in the [gexf format](https://gexf.net/)
    """
    G = export_networkX_from_arepo()
    # saving graph created above in gexf format
    nx.write_gexf(G, filename +  ".gexf")

def export_graphml_from_arepo(filename:str):
    """
    It read article repository and extract node & edge from it and exports it as a [graphml file](http://graphml.graphdrawing.org/)
    
    :param filename: the name of the file you want to save the graphml file as
    :type filename: str
    """
    G = export_networkX_from_arepo()
    # saving graph created above in graphml format
    nx.write_graphml(G, filename + ".graphml")

def export_graphml_from_networkx(G:nx.Graph, filename:str):
    """
    It takes a networkx graph and a filename, and exports the graph to a graphml file with the given
    filename
    
    :param G: the networkx graph object
    :type G: nx.Graph
    :param filename: the name of the file you want to save the graph as
    :type filename: str
    """
    nx.write_graphml(G, filename + ".graphml")

##-------------------------------------------------------------------------------------------------------------
def export_networkX(nodes : list[Node] , edges : list[Edge], graph_type: Optional[str] = 'directed' ):
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

def export_networkX(nodes : list[dict] , edges : list[dict], graph_type: Optional[str] = 'directed' ):
    if graph_type == 'undirected':
        G = nx.Graph()
    elif graph_type == 'directed':
        G = nx.DiGraph()
    else:
        raise NotImplementedError

    # nodes = get_all_nodes()
    for node in nodes:
        # node = Node(**n.copy()) 
        G.add_node(node['Identifier'] , Type = node['Type'], Name = node['Name'])

    # edges = get_all_edges()
    for edge in edges:
        # edge = Edge(**e.copy()) 
        G.add_edge(edge['SourceID'] , edge['DestinationID'] , Type = edge['Type'])

    return G


from triplea.config.settings import ROOT
import pandas as pd
# from nams.solutions.hubs import ecdf_degree
if __name__ == '__main__':
    pass
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





