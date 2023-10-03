


from pymongo import MongoClient
from tests.fixtures.graph_52 import graph52_instance
from triplea.cli import export_graph

import triplea.cli as cli
from triplea.config.settings import SETTINGS

from triplea.service.repository.import_file.triplea import import_triplea_json

from triplea.service.graph.analysis.ganalysis import get_avg_shortest_path_length_per_node, get_clustering_coefficient_per_node
import networkx as nx

from triplea.utils.general import safe_csv


if __name__ == "__main__":
    pass
    # text='Schizophrenia, "Just the Facts": what we know in 2008 part 1: overview '
    # print(safe_csv(text))

    _connection_url = SETTINGS.AAA_MONGODB_CONNECTION_URL
    client = MongoClient(_connection_url)
    db = client[SETTINGS.AAA_MONGODB_DB_NAME]
    col_article = db["articledata"]
    col_nodes = db["nodes"]
    col_edges = db["edges"]
    col_triple = db["triple"]
    myquery = {"FlagExtractTopic": 0}
    sett = {"$set": {"Topics": []}}
    r = col_article.update_many(myquery, sett)
 



