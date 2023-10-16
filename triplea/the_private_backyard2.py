# flake8: noqa
# noqa: F401

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

if __name__ == "__main__":
    pass
    export_triplea_csvs_in_relational_mode_save_file(
        "export.csv", proccess_bar=True, limit_sample=0
    )

    # move_state_forward(2)
    # go_affiliation_mining()

    # persist.change_flag_extract_topic(1,0)
    # go_extract_topic(proccess_bar=True)

    # aff_text = "Institute for Molecular Medicine Finland (FIMM), Helsinki Institute of Life Science (HiLIFE), University of Helsinki, Helsinki, Finland. aarno.palotie@helsinki.fi"
    # aff_text = "Department of Neurology and Institute of Neurology, Huashan Hospital, State Key Laboratory of Medical Neurobiology and MOE Frontiers Center for Brain Science, Shanghai Medical College, Fudan University, National Center for Neurological Disorders, Shanghai, China. jintai_yu@fudan.edu.cn"
    # aff_text = "Department of Ophthalmology, University of Washington, Seattle, Washington, USA"
    # print(get_affiliation_structured(aff_text))

    # from triplea.service.repository.state.custom.affiliation_mining import _is_country
    # print(_is_country("Finland. aarno.palotie@helsinki.fi"))
    # print(_is_country("Finland"))

    # print(parse_affiliation(aff_text))

    # go_affiliation_mining(method='Titipata')

    # import triplea.service.repository.state as state_manager
    # a = persist.get_article_by_pmid('31679581')
    # updated_article = Article(**a.copy())
    # state_manager.affiliation_mining_titipata(updated_article)

    # import triplea.service.repository.state as state_manager
    # a = persist.get_article_by_pmid('34358588')
    # updated_article = Article(**a.copy())
    # state_manager.parsing_details(updated_article)
