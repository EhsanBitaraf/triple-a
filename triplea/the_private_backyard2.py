# flake8: noqa
# noqa: F401

from bson import BSON, ObjectId
import click
import time
import sys
import json
import re
import networkx as nx
from pymongo import MongoClient
from triplea.client.affiliation_parser import parse_affiliation
from triplea.config.settings import SETTINGS, ROOT
from triplea.service.click_logger import logger
from triplea.schemas.article import Article
from triplea.schemas.node import Node
from triplea.service.graph.analysis.info import info
from triplea.service.repository.export.llm import export_pretrain_llm_in_dir
from triplea.service.repository.export.triplea_format import (
    export_triplea_csvs_in_relational_mode_save_file,
)
import triplea.service.repository.persist as persist
import triplea.service.graph.export.export as gexport
import triplea.service.graph.analysis.ganalysis as ganaliz
import traceback
import os

from triplea.service.repository.pipeline_core import move_state_forward
from triplea.service.repository.pipeline_flag import (
    go_affiliation_mining,
    go_extract_topic,
)
from triplea.service.repository.state.custom.affiliation_mining import (
    get_affiliation_structured,
)
from triplea.service.repository.state.initial_arxiv import get_article_list_from_arxiv_all_store_to_arepo
from triplea.service.repository.state.initial import get_article_list_from_pubmed_all_store_to_arepo
if __name__ == "__main__":
    pass

    # Pipeline Sample

    # # Step 1 - Get article from Arxiv
    # arxiv_search_string = 'ti:"large language model" AND ti:Benchmark'
    # get_article_list_from_arxiv_all_store_to_arepo(arxiv_search_string,0,10)

    # # Step 2 - Get article from Pubmed
    # pubmed_search_string = '("large language model"[Title]) AND (Benchmark[Title/Abstract])'
    # get_article_list_from_pubmed_all_store_to_arepo(pubmed_search_string)
 


    # Step 3 - Get info
    persist.print_article_info_from_repo()

    # # Step 4 - Moving from `0` to `1`
    # move_state_forward(0)                    

    # # Step 5 - Moving from `1` to `2`
    # move_state_forward(1)
                    
    # # Step 6 - Moving from `2` to `3`
    # move_state_forward(2)
                    
    # Get article info
    # print()               
    # persist.print_article_short_description("37567487","pmid")

    
    # a = persist.get_article_by_id(ObjectId('658f85228f23534d63358a19'))
    # updated_article = Article(**a.copy())
    # print(updated_article.State)
    # print(updated_article.Title)
    # print(updated_article.Published)
    # print(type(updated_article.Published))

    import triplea.service.repository.pipeline_flag as cPIPELINE

    # cPIPELINE.go_extract_topic()

    # cPIPELINE.go_affiliation_mining(method="Titipata")

    # cPIPELINE.go_extract_triple()

    export_triplea_csvs_in_relational_mode_save_file("export")
    