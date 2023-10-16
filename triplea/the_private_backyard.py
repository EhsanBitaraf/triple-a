# flake8: noqa


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
from triplea.cli.export_graph import export_graph
from triplea.client.topic_extraction import extract_topic
from triplea.schemas.article import Article
from triplea.service.graph import extract

import triplea.service.graph.analysis.ganalysis as ganaliz
import triplea.service.graph.export.export as gexport
import triplea.service.graph.extract as gextract

# import triplea.service.graph.export as gexport
from triplea.service.graph.extract import Emmanuel, check_upper_term, _t_emmanuel
from triplea.service.click_logger import logger
from triplea.service.graph.extract.country_based_co_authorship import (
    graph_extract_article_country,
)
import triplea.service.repository.persist as persist
from triplea.service.repository.pipeline_core import move_state_forward
from triplea.service.repository.pipeline_flag import go_extract_topic, go_extract_triple
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
    pass

    # remove_duplicate = True
    # format_type = "graphdict"
    # proccess_bar = False
    # output_file = "topic.json"

    # l_nodes = []
    # l_edges = []
    # graphdict = gextract.graph_extractor(
    #     gextract.graph_extract_article_topic,
    #     proccess_bar=proccess_bar,
    #     remove_duplicate=remove_duplicate,
    # )
    # l_nodes.extend(graphdict["nodes"])
    # l_edges.extend(graphdict["edges"])
    # logger.DEBUG("Save temp file with duplication.")
    # data = json.dumps({"nodes": l_nodes, "edges": l_edges}, indent=4)
    # with open("temp-with-duplication.json", "w") as outfile:
    #     outfile.write(data)
    #     outfile.close()
    # if remove_duplicate:
    #     logger.DEBUG("Remove duplication in Nodes & Edges. ")
    #     n = gextract.thefourtheye_2(l_nodes)
    #     e = gextract.thefourtheye_2(l_edges)

    #     n = list(n)
    #     e = list(e)
    #     graphdict = {"nodes": n, "edges": e}
    # else:
    #     graphdict = {"nodes": l_nodes, "edges": l_edges}

    # if format_type == "graphdict":
    #     data1 = json.dumps(graphdict, indent=4)
    #     with open(output_file, "w") as outfile:
    #         outfile.write(data1)

    # import visualization.gdatarefresh as graphdatarefresh
    # file = "topic1.json"
    # with open(file, "r") as f:
    #     graphdict = json.load(f)
    # graphdatarefresh.refresh_interactivegraph(graphdict)
    # graphdatarefresh.refresh_alchemy(graphdict)

    l_pmid = persist.get_all_article_pmid_list()
    total_article_in_current_state = len(l_pmid)
    number_of_article_move_forward = 0
    logger.DEBUG(str(len(l_pmid)) + " Article(s) is in FlagAffiliationMining " + str(0))

    bar = click.progressbar(length=len(l_pmid), show_pos=True, show_percent=True)

    refresh_point = 0
    for id in l_pmid:
        start_time = time.time()
        try:
            number_of_article_move_forward = number_of_article_move_forward + 1

            if refresh_point == 50:
                refresh_point = 0
                persist.refresh()
                print()
                logger.INFO(
                    f"There are {str(total_article_in_current_state - number_of_article_move_forward)} article(s) left ",
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

            if updated_article.Authors is not None:
                for a in updated_article.Authors:
                    if a.Affiliations is not None:
                        for aff in a.Affiliations:
                            aff.Structural = None

            persist.update_article_by_pmid(updated_article, updated_article.PMID)

            # logger.DEBUG('Article ' + updated_article.PMID + ' with state ' + str(current_state) + ' forward to ' + str(current_state + 1))
            bar.label = "Article " + updated_article.PMID + " affiliation mining."
            bar.update(1)
            # # for re run
            # if current_state == 2 : current_state = 1

        except Exception:
            persist.refresh()
            exc_type, exc_value, exc_tb = sys.exc_info()
            print()
            print(exc_tb.tb_lineno)
            logger.ERROR(f"Error {exc_type}")
            logger.ERROR(f"Error {exc_value}")
    persist.refresh()
