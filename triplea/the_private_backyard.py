import time
import networkx as nx

# import nxviz as nv??
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from netwulf import visualize

import json
from triplea.service.graph import extract

import triplea.service.graph.analysis.ganalysis as ganaliz
import triplea.service.graph.export.export as gexport
import triplea.service.graph.extract as gextract

# import triplea.service.graph.export as gexport
from triplea.service.graph.extract import Emmanuel, check_upper_term, _t_emmanuel
from triplea.service.click_logger import logger
import triplea.service.repository.persist as persist

def check_map_topic():
    f = open("one-graph.json")
    data = json.load(f)
    f.close()
    new_nodes = []
    new_edges = []
    for n in data["nodes"]:
        if n["Type"] == "Topic":
            uv = check_upper_term(n, "cancer")
            if uv is not None:
                new_nodes.append(uv["node"])
                new_edges.append(uv["edge"])

            uv = check_upper_term(n, "breast")
            if uv is not None:
                new_nodes.append(uv["node"])
                new_edges.append(uv["edge"])

            uv = check_upper_term(n, "registry")
            if uv is not None:
                new_nodes.append(uv["node"])
                new_edges.append(uv["edge"])

            uv = check_upper_term(n, "data")
            if uv is not None:
                new_nodes.append(uv["node"])
                new_edges.append(uv["edge"])

    n = Emmanuel(new_nodes)
    e = Emmanuel(new_edges)
    data["nodes"].extend(n)
    data["edges"].extend(e)

    G = gexport.export_networkx_from_graphdict(data)
    ganaliz.info(G)


if __name__ == "__main__":
    l_pmid = persist.get_article_pmid_list_by_cstate(None,"cstate")
    print(len(l_pmid))