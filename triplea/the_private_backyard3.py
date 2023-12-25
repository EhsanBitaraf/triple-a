# flake8: noqa
# noqa: F401

from triplea.service.repository.state.initial import get_article_list_from_pubmed_all_store_to_arepo

import array
from pymongo import MongoClient
from tests.fixtures.graph_52 import graph52_instance
from triplea.cli import export_graph

import triplea.cli as cli
from triplea.config.settings import SETTINGS

from triplea.service.repository.import_file.triplea import import_triplea_json

from triplea.service.graph.analysis.ganalysis import (
    get_avg_shortest_path_length_per_node,
    get_clustering_coefficient_per_node,
)
import networkx as nx

from triplea.utils.general import safe_csv


if __name__ == "__main__":
    term = '("Large Language Models"[Title/Abstract]) OR ("Large Language Model"[Title/Abstract]) OR (LLM[Title/Abstract]) OR (LLMs[Title/Abstract]) OR (ChatGPT[Title/Abstract])'
    get_article_list_from_pubmed_all_store_to_arepo(term)
