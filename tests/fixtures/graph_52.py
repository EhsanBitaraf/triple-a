
import os
import pytest
import networkx as nx

from triplea.config.settings import ROOT


"""
This is a pytest fixture that sets up a graph object by reading a graphml file.
52 Article(s) 
979 Nodes & 1466 Edges
"""
@pytest.fixture
def graph52():
    # set up code goes here
    try:
        path_graph = os.path.join(ROOT.parent, "tests" , "fixtures","g52.graphml")
        G = nx.read_graphml(path_graph)
        # G = nx.read_graphml('tests\\fixtures\\g52.graphml')
    except FileNotFoundError:
        G = nx.read_graphml('g52.graphml')
        print("File 'g52.graphml' does not exist.")
        return G
    except nx.NetworkXError:
        print("Error reading 'g52.graphml' file.")
    else:
        return G


def graph52_instance():
    # set up code goes here
    try:
        path_graph = os.path.join(ROOT.parent, "tests" , "fixtures","g52.graphml")
        G = nx.read_graphml(path_graph)
        # G = nx.read_graphml('tests\\fixtures\\g52.graphml')
    except FileNotFoundError:
        G = nx.read_graphml('g52.graphml')
        print("File 'g52.graphml' does not exist.")
        return G
    except nx.NetworkXError:
        print("Error reading 'g52.graphml' file.")
    else:
        return G
    


   