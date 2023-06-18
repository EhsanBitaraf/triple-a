import sys
import time
import networkx as nx

# import nxviz as nv??
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from netwulf import visualize
import click

import json
from triplea.schemas.article import Article
from triplea.service.graph import extract

import triplea.service.graph.analysis.ganalysis as ganaliz
import triplea.service.graph.export.export as gexport
import triplea.service.graph.extract as gextract

# import triplea.service.graph.export as gexport
from triplea.service.graph.extract import Emmanuel, check_upper_term, _t_emmanuel
from triplea.service.click_logger import logger
from triplea.service.graph.extract.country_based_co_authorship import graph_extract_article_country
import triplea.service.repository.persist as persist
import triplea.service.repository.state as state_manager
from triplea.service.repository.state.custom.affiliation_mining import country_list



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
    a = persist.get_article_by_pmid('37115160')
    updated_article = Article(**a.copy())
    # graph_extract_article_country(updated_article)
    updated_article = state_manager.extract_topic_abstract(updated_article)

    l_pmid = persist.get_article_pmid_list_by_cstate( 0, "FlagExtractTopic" )
    total_article_in_current_state = len(l_pmid)
    number_of_article_move_forward = 0
    logger.DEBUG(str(len(l_pmid)) + " Article(s) is in FlagExtractTopic " + str(0))

    bar = click.progressbar(length=len(l_pmid), show_pos=True, show_percent=True)

    refresh_point = 0
    elapsed = 0
    for id in l_pmid:
        start_time = time.time()
        try:
            number_of_article_move_forward = number_of_article_move_forward + 1
            current_state = None

            if refresh_point == 50:
                refresh_point = 0
                persist.refresh()
                print()
                logger.INFO(
                    f"There are {str(total_article_in_current_state - number_of_article_move_forward)} article(s) left ",
                    forecolore="yellow",
                )
                min = (
                    (total_article_in_current_state - number_of_article_move_forward) * elapsed
                ) / 60
                logger.INFO(
                    f"It takes at least {str(int(min))} minutes or {str(int(min/60))} hours",
                    forecolore="yellow",
                )
            else:
                refresh_point = refresh_point + 1

            a = persist.get_article_by_pmid(id)
            try:
                updated_article = Article(**a.copy())
            except Exception:
                print()
                print(logger.ERROR(f"Error in parsing article. PMID = {id}"))
                raise Exception("Article Not Parsed.")
            try:
                current_state = updated_article.FlagExtractTopic #----------------------------------------------------
            except Exception:
                current_state = 0

            bar.label = (
                "Article "
                + updated_article.PMID
                + " , topic were extracted."
            )
            bar.update(1)

            if current_state is None:
                updated_article = state_manager.extract_topic_abstract(updated_article)
                persist.update_article_by_pmid(updated_article,
                                                updated_article.PMID)

            elif current_state == -1:  
                updated_article = state_manager.extract_topic_abstract(updated_article)
                persist.update_article_by_pmid(updated_article,
                                                updated_article.PMID)

            elif current_state == 0:  
                updated_article = state_manager.extract_topic_abstract(updated_article)
                persist.update_article_by_pmid(updated_article,
                                               updated_article.PMID)

            elif current_state == 1:  
                pass

            else:
                raise NotImplementedError

        except Exception:
            if current_state == 0 or current_state is None:
                updated_article = Article(**a.copy())
                updated_article.State = -1
                persist.update_article_by_pmid(updated_article,
                                                updated_article.PMID)
                persist.refresh()
                exc_type, exc_value, exc_tb = sys.exc_info()
                print()
                logger.ERROR(f"Error {exc_type}")
                logger.ERROR(f"Error {exc_value}")

            else:
                persist.refresh()
                exc_type, exc_value, exc_tb = sys.exc_info()
                print()
                print(exc_tb.tb_lineno)
                logger.ERROR(f"Error {exc_type}")
                logger.ERROR(f"Error {exc_value}")
        elapsed = time.time() - start_time
    persist.refresh()