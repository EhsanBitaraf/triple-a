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
from triplea.service.repository.state.initial_arxiv import (
    get_article_list_from_arxiv_all_store_to_arepo,
)
from triplea.service.repository.state.initial import (
    get_article_list_from_pubmed_all_store_to_arepo,
)


if __name__ == "__main__":
    pass
