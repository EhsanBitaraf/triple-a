# flake8: noqa
# noqa: F401

import json
from triplea.client.arxiv import get_article_list_from_arxiv
from triplea.schemas.article import Article, Author
from triplea.service.repository import persist
from triplea.service.repository.pipeline_core import move_state_forward
from triplea.service.repository.pipeline_flag import go_article_embedding
from triplea.service.repository.state.initial import (
    get_article_list_from_pubmed_all_store_to_arepo,
)

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
from triplea.service.repository.state.initial_arxiv import (
    get_article_list_from_arxiv_all_store_to_arepo,
)

from triplea.utils.general import safe_csv


if __name__ == "__main__":
    pass
    # term = '("Large Language Models"[Title/Abstract]) OR ("Large Language Model"[Title/Abstract]) OR (LLM[Title/Abstract]) OR (LLMs[Title/Abstract]) OR (ChatGPT[Title/Abstract])'
    # get_article_list_from_pubmed_all_store_to_arepo(term)

    # r = get_article_list_from_arxiv("all:model", 1 ,3)
    # with open("temp-arxiv.json", "w") as outfile:
    #     outfile.write(json.dumps(r, indent=4, sort_keys=True))
    #     outfile.close()

    # get_article_list_from_arxiv_all_store_to_arepo("all:electron", 1 ,3)

    # from triplea.config.settings import SETTINGS
    # import json
    # import triplea.utils as Utils

    # f = open('temp-arxiv.json')
    # data = json.load(f)
    # a = int (data["feed"]["opensearch:totalResults"]["#text"])
    # print(data["feed"]["opensearch:totalResults"]["#text"])
    # print(a+1)
    # import urllib.parse

    # text= 'ti:"large language model" OR abs:"medical"'
    # text= urllib.parse.quote(text)
    # get_article_list_from_arxiv_all_store_to_arepo(text,20,10)

    # data = persist.get_article_group_by_state()
    # print(data)

    # move_state_forward(-1)

    # move_state_forward(0)
    go_article_embedding()
