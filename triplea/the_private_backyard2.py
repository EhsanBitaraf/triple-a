
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
import triplea.service.repository.persist as persist
import triplea.service.graph.export.export as gexport
import triplea.service.graph.analysis.ganalysis as ganaliz
import traceback
import os

if __name__ == "__main__":
    pass
    state = 2
    proccess_bar = True
    limit_node = 100
    path = 'export4llm'
    if state is None:
        l_pmid = persist.get_all_article_pmid_list()
        logger.INFO(str(len(l_pmid)) + " Article(s) ")
    else:
        l_pmid = persist.get_article_pmid_list_by_state(state)
        logger.INFO(str(len(l_pmid)) + " Article(s) is in state " + str(state))

    n = 0
    if proccess_bar:
        bar = click.progressbar(length=len(l_pmid), show_pos=True, show_percent=True)

    if os.path.exists(ROOT / path ):
        pass
    else:
        os.mkdir(ROOT / path)

    for id in l_pmid:
        n = n + 1
        if proccess_bar:
            bar.update(1)
        a = persist.get_article_by_pmid(id)
        try:
            article = Article(**a.copy())
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            print()
            logger.ERROR(f"Error {exc_type}")
            logger.ERROR(f"Error {exc_value}")
            # logger.ERROR(f'Error {exc_tb.tb_next}')
            article = None

        if limit_node != 0:  # Unlimited
            if n == limit_node:
                pass
                
                # for temp
                # return 



        if article is not None:
            if article.Abstract is not None:
                #or article != ""
                f = open(ROOT / path / f"{article.PMID}.txt", "w", encoding='utf-8')
                f.write(article.Abstract)
                f.close()

                if proccess_bar:
                    bar.label = f"Article ({n}) (PMID : {article.PMID}): Save Abstract)"
            else:
                print()
                print("Article is None!")
                

    # return

