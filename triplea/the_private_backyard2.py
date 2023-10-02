
import click
import time
import sys
import json
import re
import networkx as nx
from pymongo import MongoClient
from triplea.config.settings import SETTINGS,ROOT
from triplea.service.click_logger import logger
from triplea.schemas.article import Article
from triplea.schemas.node import Node
from triplea.service.graph.analysis.info import info
from triplea.service.repository.export.llm import export_pretrain_llm_in_dir
from triplea.service.repository.export.triplea_format import export_triplea_csvs_in_relational_mode_save_file
import triplea.service.repository.persist as persist
import triplea.service.graph.export.export as gexport
import triplea.service.graph.analysis.ganalysis as ganaliz
import traceback
import os

from triplea.service.repository.pipeline_core import move_state_forward
from triplea.service.repository.pipeline_flag import go_affiliation_mining, go_extract_topic

if __name__ == "__main__":
    pass
    export_triplea_csvs_in_relational_mode_save_file('export.csv',
                                                     proccess_bar=True)
    # move_state_forward(2)
    # go_affiliation_mining()
    # go_extract_topic(proccess_bar=True)
