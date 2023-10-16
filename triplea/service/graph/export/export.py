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
            print(
                f'{n} | DestinationID "{edge.DestinationID}" Not Exist. in Type : {edge.Type} & SourceID =  "{edge.SourceID}"'
            )


def export_graphjson_from_graphdict(graphdict) -> dict:
    """
    It takes a graphdict and returns a graphjson
    we use graphjson in alchemy visualization

    :param graphdict: The graph dictionary that you want to export
    :return: A dictionary
    """
    data = {}
    data["comment"] = "This file generate autommaticlly by TripleA"
    nodes = graphdict["nodes"]
    data_nodes = []
    for n in nodes:
        data_n = {}
        data_n["caption"] = n["Name"]
        data_n["type"] = n["Type"]
        data_n["id"] = n["Identifier"]
        data_nodes.append(data_n)

    edges = graphdict["edges"]
    data_edges = []
    for e in edges:
        data_e = {}
        data_e["source"] = e["SourceID"]
        data_e["target"] = e["DestinationID"]
        data_e["caption"] = e["Type"]
        data_edges.append(data_e)

    data["nodes"] = data_nodes
    data["edges"] = data_edges
    return data


def export_graphjson_from_arepo() -> dict:
    """
    It takes all the nodes and edges from the article repository and converts them into a format that can be used
    by the graph visualization library
    :return: A dictionary with two keys: nodes and edges.
    """
    data = {}
    data["comment"] = "This file generate autommaticlly by TripleA"
    nodes = persist.get_all_nodes()
    data_nodes = []
    for n in nodes:
        node = Node(**n.copy())
        data_n = {}
        data_n["caption"] = node.Name
        data_n["type"] = node.Type
        data_n["id"] = node.Identifier
        data_nodes.append(data_n)

    edges = persist.get_all_edges()
    data_edges = []
    for e in edges:
        edge = Edge(**e.copy())
        data_e = {}
        data_e["source"] = edge.SourceID
        data_e["target"] = edge.DestinationID
        data_e["caption"] = edge.Type
        data_edges.append(data_e)

    data["nodes"] = data_nodes
    data["edges"] = data_edges
    return data


def export_networkX_from_arepo(graph_type: Optional[str] = "directed"):
    """
    It takes a list of nodes and edges from the article repository and creates a networkX graph object
    :return: A networkx graph object
    """
    if graph_type == "undirected":
        G = nx.Graph()
    elif graph_type == "directed":
        G = nx.DiGraph()
    else:
        raise NotImplementedError

    nodes = persist.get_all_nodes()
    for n in nodes:
        node = Node(**n.copy())
        G.add_node(node.Identifier, Type=node.Type, Name=node.Name)

    edges = persist.get_all_edges()
    for e in edges:
        edge = Edge(**e.copy())
        G.add_edge(edge.SourceID, edge.DestinationID, Type=edge.Type)

    return G


def export_gpickle_from_arepo(filename: str):
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


def export_gpickle_from_graphdict(graphdict: dict, filename: str):
    """
    It takes a graph dictionary and exports it as a gpickle file

    :param graphdict: a dictionary of dictionaries, where the keys are the nodes and the values are
    dictionaries of the node's neighbors and their weights
    :type graphdict: dict
    :param filename: the name of the file you want to save the graph to
    :type filename: str
    """
    G = export_networkx_from_graphdict(graphdict)
    nx.write_gpickle(G, filename)


def export_gexf_from_arepo(filename: str):
    """
    It read article repository and extract node & edge from it,
    and then saves it in the [gexf format](https://gexf.net/)
    """
    G = export_networkX_from_arepo()
    # saving graph created above in gexf format
    nx.write_gexf(G, filename)


def export_gexf_from_graphdict(graphdict: dict, filename: str):
    """
    It takes a graph dictionary and exports it as a GEXF file

    :param graphdict: a dictionary of dictionaries,
      where the keys are the nodes and the values are
    dictionaries of the nodes' neighbors and the weights of the edges
      between them
    :type graphdict: dict
    :param filename: the name of the file you want to save the graph as
    :type filename: str
    """
    G = export_networkx_from_graphdict(graphdict)
    nx.write_gexf(G, filename)


def export_graphml_from_arepo(filename: str):
    """
    It read article repository and extract node & edge from it
      and exports it as a [graphml file](http://graphml.graphdrawing.org/)

    :param filename: the name of the file you want to save the graphml file as
    :type filename: str
    """
    G = export_networkX_from_arepo()
    # saving graph created above in graphml format
    nx.write_graphml(G, filename)


def export_graphml_from_networkx(G: nx.Graph, filename: str):
    """
    It takes a networkx graph and a filename, and exports the graph
      to a graphml file with the given
    filename

    :param G: the networkx graph object
    :type G: nx.Graph
    :param filename: the name of the file you want to save the graph as
    :type filename: str
    """
    nx.write_graphml(G, filename)


def export_graphml_from_graphdict(graphdict: dict, filename: str):
    """
    It takes a graph dictionary and exports it to a graphml file

    :param filename: the name of the file you want to save the graphml file as
    :type filename: str
    """
    G = export_networkx_from_graphdict(graphdict)
    nx.write_graphml(G, filename)


def export_gson_from_graphdict(graphdict) -> dict:
    """
    > It takes a graph dictionary and returns a GSON format
    we use GSON format in interactivegraph visualization

    :param graphdict: the graph dictionary
    :return: A dictionary with GSON format
    """
    gson_nodes = []
    gson_edges = []
    for n in graphdict["nodes"]:
        gson_node = {}
        gson_node["label"] = n["Name"]
        gson_node["id"] = n["Identifier"]
        # gson_node['info'] = title ...
        # gson_node['value'] = degree ...
        # gson_node['image']
        # gson_node['categories']
        # gson_node['community']
        # gson_node['group']
        # gson_node['x']
        # gson_node['y']
        gson_node["categories"] = {n["Type"]: n["Type"]}
        if n["Type"] == "Article":
            gson_node["value"] = 10
            gson_node["image"] = "./images/photo/article.png"
        elif n["Type"] == "Author":
            gson_node["value"] = 5
            gson_node["image"] = "./images/photo/author.png"
        elif n["Type"] == "Affiliation":
            gson_node["value"] = 15
            gson_node["image"] = "./images/photo/institute.png"
        elif n["Type"] == "Keyword":
            gson_node["value"] = 15
            # gson_node['image'] = "./images/photo/institute.png"
        elif n["Type"] == "Topic":
            gson_node["value"] = 15
            # gson_node['image'] = "./images/photo/institute.png"
        else:
            gson_node["value"] = 1

        gson_nodes.append(gson_node)

    for e in graphdict["edges"]:
        gson_edge = {}
        gson_edge["id"] = e["HashID"]
        gson_edge["from"] = e["SourceID"]
        gson_edge["to"] = e["DestinationID"]
        gson_edge["label"] = e["Type"]
        gson_edges.append(gson_edge)

    result = {}
    result["data"] = {"nodes": gson_nodes, "edges": gson_edges}
    return result


def export_networkx_from_graphdict(
    graphdict, graph_type: Optional[str] = "directed"
) -> nx.Graph:
    """
    It takes a graph dictionary and returns a networkx graph

    :param graphdict: The graph dictionary that you want to convert
      to a networkx graph
    :param graph_type: Optional[str] = 'directed', defaults to directed
    :type graph_type: Optional[str] (optional)
    :return: A networkx graph object
    """
    if graph_type == "undirected":
        G = nx.Graph()
    elif graph_type == "directed":
        G = nx.DiGraph()
    else:
        raise NotImplementedError

    for node in graphdict["nodes"]:
        G.add_node(node["Identifier"], Type=node["Type"], Name=node["Name"])

    for edge in graphdict["edges"]:
        G.add_edge(edge["SourceID"], edge["DestinationID"], Type=edge["Type"])

    return G


# #----------------------------------------------------------------------------
def export_networkX(
    nodes: list[Node], edges: list[Edge], graph_type: Optional[str] = "directed"
):
    if graph_type == "undirected":
        G = nx.Graph()
    elif graph_type == "directed":
        G = nx.DiGraph()
    else:
        raise NotImplementedError

    # nodes = get_all_nodes()
    for node in nodes:
        # node = Node(**n.copy())
        G.add_node(node.Identifier, Type=node.Type, Name=node.Name)

    # edges = get_all_edges()
    for edge in edges:
        # edge = Edge(**e.copy())
        G.add_edge(edge.SourceID, edge.DestinationID, Type=edge.Type)

    return G


if __name__ == "__main__":
    pass
    # export_networkX()
    # export_gexf('ehr')
    # export_graphml('ehr')

    # # check integrity of graph
    # _check_graph()

    # print(ROOT.parent / 'visualization' / 'alchemy' / 'data.json')

    # # Export All
    # state = 2
    # graphdict1 = graph_extractor(graph_extract_article_author_affiliation, state)
    # graphdict2 = graph_extractor(graph_extract_article_topic, state)
    # graphdict3 = graph_extractor(graph_extract_article_keyword, state)
    # graphdict4 = graph_extractor(graph_extract_article_reference, state)
    # # graphdict5 = graph_extractor(graph_extract_article_cited, state)
    # nodes = []
    # nodes.extend(graphdict1['nodes'])
    # nodes.extend(graphdict2['nodes'])
    # nodes.extend(graphdict3['nodes'])
    # nodes.extend(graphdict4['nodes'])
    # # nodes.extend(graphdict5['nodes'])
    # edges = []
    # edges.extend(graphdict1['edges'])
    # edges.extend(graphdict2['edges'])
    # edges.extend(graphdict3['edges'])
    # edges.extend(graphdict4['edges'])
    # # edges.extend(graphdict5['edges'])

    # n = Emmanuel(nodes)
    # e = Emmanuel(edges)
    # logger.DEBUG(f'Final {len(n)} Nodes & {len(e)} Edges Extracted.')
    # graphdict = { 'nodes' : n , 'edges' : e}
