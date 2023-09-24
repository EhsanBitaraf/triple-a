
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
import triplea.service.repository.persist as persist
import triplea.service.graph.export.export as gexport
import triplea.service.graph.analysis.ganalysis as ganaliz
import traceback
import os

if __name__ == "__main__":
    pass
    # export_pretrain_llm_in_dir(r"C:\Users\Bitaraf\Desktop\ff\hgj\i90",Merge=True,proccess_bar=True,limit_sample=0)

    output_file = r"C:\Users\Bitaraf\Desktop\ff\hgj\i90\a.text"
    file_name = os.path.basename(output_file)
    file = os.path.splitext(file_name)
    fname = file[0] 
    fextention = file[1]


    dir = output_file.replace(fname + fextention, '')
    if fextention is None:
        fextention= '.csv'

    print(dir)