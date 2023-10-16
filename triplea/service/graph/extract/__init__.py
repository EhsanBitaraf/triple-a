import json
import sys
import time
import click
import threading
from typing import Optional
from triplea.schemas.article import Article
import triplea.service.repository.persist as persist
from triplea.service.click_logger import logger

from triplea.service.graph.extract.topic import graph_extract_article_topic
from triplea.service.graph.extract.author import (
    graph_extract_article_author_affiliation,
)
from triplea.service.graph.extract.keyword import graph_extract_article_keyword
from triplea.service.graph.extract.reference import graph_extract_article_reference
from triplea.service.graph.extract.cited import graph_extract_article_cited
from triplea.service.graph.extract.country_based_co_authorship import (
    graph_extract_article_country,
)


__all__ = [
    "graph_extractor",
    "graph_extract_article_topic",
    "graph_extract_article_author_affiliation",
    "graph_extract_article_keyword",
    "graph_extract_article_reference",
    "graph_extract_article_cited",
    "graph_extract_article_country",
]


class _tdedup:
    def __init__(self, d):
        self.d = d
        self.new_l = []

    def run(self, i, n):
        if i not in self.d[n + 1 :]:
            self.new_l.append(i)

    def get_new_l(self):
        return self.new_l


def _t_emmanuel(d: list) -> list:
    start_time = time.time()
    new_l = []

    tdedup = _tdedup(d)

    total = len(d)
    bar = click.progressbar(length=total, show_pos=True, show_percent=True)
    threads = []
    t_q_num = 1
    t_num = 1
    for n, i in enumerate(d):
        bar.update(1)
        bar.label = f"Scan for remove duplication what : {threading.activeCount()} {str(len(threads))}"

        t1 = threading.Thread(
            target=tdedup.run,
            args=(
                i,
                n,
            ),
        )
        t1.start()
        threads.append(t1)
        t_num = t_num + 1

        if t_num > t_q_num:
            for t in threads:
                t.join()
            t_num = 0
            threads = []

    print()
    process_time = time.time() - start_time
    logger.INFO(f"process_time : {str(process_time)}")
    return new_l


def Emmanuel(d: list) -> list:
    """Base on [this](https://stackoverflow.com/questions/9427163/remove-duplicate-dict-in-list-in-python)

    Args:
        d (list): _description_

    Returns:
        list: _description_
    """
    return [i for n, i in enumerate(d) if i not in d[n + 1 :]]


def _emmanuel(d: list) -> list:
    """Base on [this](https://stackoverflow.com/questions/9427163/remove-duplicate-dict-in-list-in-python)

    Args:
        d (list): _description_

    Returns:
        list: _description_

    """
    start_time = time.time()
    # response = await call_next(request)
    new_l = []
    total = len(d)
    bar = click.progressbar(length=total, show_pos=True, show_percent=True)
    p_total_num = total / 100
    P_num = 0
    for n, i in enumerate(d):
        P_num = P_num + 1
        if P_num > p_total_num:
            bar.update(P_num)
            bar.label = "Scan for remove duplication "
            P_num = 0
        if i not in d[n + 1 :]:
            new_l.append(i)

    bar.finish()
    print()
    process_time = time.time() - start_time
    logger.INFO(f"process_time : {str(process_time)}")
    return new_l


def thefourtheye_2(data):
    """
    It takes a list of dictionaries, converts each dictionary to a frozenset of tuples, and then uses
    the frozenset as a key in a dictionary, with the value being the original dictionary
    Base on [this](https://stackoverflow.com/questions/9427163/remove-duplicate-dict-in-list-in-python)

    :param data: The list of dictionaries that you want to remove duplicates from
    :return: A dictionary with the keys being the frozenset of the items in the list and the values
    being the items in the list.
    """
    return {frozenset(item.items()): item for item in data}.values()


def graph_extractor(
    func,
    state: Optional[int] = None,
    limit_node: Optional[int] = 0,
    proccess_bar: Optional[bool] = True,
    remove_duplicate: Optional[bool] = True,
):
    """
    It takes a function as an argument, and returns a dictionary of nodes and edges

    :param func: the function that will be used to extract the graph from the article
    :param state: the state of the article, which is an integer
    :type state: int
    :return: A dictionary with two keys, 'nodes' and 'edges'. The values are remove duplicate nodes & edge with Emmanuel algoritm.
    """
    if state is None:
        l_pmid = persist.get_all_article_pmid_list()
        logger.INFO(str(len(l_pmid)) + " Article(s) ")
    else:
        l_pmid = persist.get_article_pmid_list_by_state(state)
        logger.INFO(str(len(l_pmid)) + " Article(s) is in state " + str(state))

    l_nodes = []
    l_edges = []
    n = 0
    if proccess_bar:
        bar = click.progressbar(length=len(l_pmid), show_pos=True, show_percent=True)
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
                # for temp
                data = json.dumps({"nodes": l_nodes, "edges": l_edges}, indent=4)
                with open("temp.json", "w") as outfile:
                    outfile.write(data)
                    outfile.close()
                if remove_duplicate:
                    print()
                    logger.DEBUG("Remove duplication in Nodes & Edges. ")
                    n = thefourtheye_2(l_nodes)
                    e = thefourtheye_2(l_edges)
                    logger.DEBUG(f"Final {len(n)} Nodes & {len(e)} Edges Extracted.")
                    return {"nodes": n, "edges": e}
                else:
                    return {"nodes": l_nodes, "edges": l_edges}

        if article is not None:
            # data = _extract_article_topic(article)
            data = func(article)
            a_nodes = data["nodes"]
            a_edges = data["edges"]
            l_nodes.extend(a_nodes)
            l_edges.extend(a_edges)
            if proccess_bar:
                bar.label = f"Article ({n}) (PMID : {article.PMID}): Extract {len(a_nodes)} Nodes & {len(a_edges)} Edges. Total ({len(l_nodes)},{len(l_edges)})"
                # logger.DEBUG(f'Article ({n}): Extract {len(a_nodes)} Nodes & {len(a_edges)} Edges. Total ({len(l_nodes)},{len(l_edges)})')

    if remove_duplicate:
        print()
        logger.DEBUG("Remove duplication in Nodes & Edges. ")
        n = thefourtheye_2(l_nodes)
        e = thefourtheye_2(l_edges)
        logger.DEBUG(f"Final {len(n)} Nodes & {len(e)} Edges Extracted.")
        return {"nodes": n, "edges": e}
    else:
        return {"nodes": l_nodes, "edges": l_edges}


def graph_extractor_all_entity(
    state: Optional[int] = None,
    limit_node: Optional[int] = 0,
    remove_duplicate: Optional[bool] = True,
):
    """
    It takes a list of articles, extracts the graph from each article, and then combines all the graphs
    into one graph.
    Graph Model contains :

    article_author_affiliation

    article_topic

    article_keyword

    article_reference

    article_cited

    :param state: The state of the article
    :type state: Optional[int]
    :param limit_node: Optional[int] = 0, defaults to 0
    :type limit_node: Optional[int] (optional)
    :return: A dictionary with two keys: nodes and edges.
    """
    if state is None:
        l_pmid = persist.get_all_article_pmid_list()
        logger.INFO(str(len(l_pmid)) + " Article(s) ")
    else:
        l_pmid = persist.get_article_pmid_list_by_state(state)
        logger.INFO(str(len(l_pmid)) + " Article(s) is in state " + str(state))
    l_nodes = []
    l_edges = []
    n = 0
    with click.progressbar(length=len(l_pmid), show_pos=True, show_percent=True) as bar:
        for id in l_pmid:
            n = n + 1
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
                    if remove_duplicate:
                        logger.DEBUG("Remove duplication in Nodes & Edges. ")
                        n = Emmanuel(l_nodes)
                        e = Emmanuel(l_edges)
                        logger.DEBUG(
                            f"Final {len(n)} Nodes & {len(e)} Edges Extracted."
                        )
                        return {"nodes": n, "edges": e}
                    else:
                        return {"nodes": l_nodes, "edges": l_edges}

            if article is not None:
                # Extracting the graph from the article.
                graphdict1 = graph_extract_article_author_affiliation(article)
                graphdict2 = graph_extract_article_topic(article)
                graphdict3 = graph_extract_article_keyword(article)
                graphdict4 = graph_extract_article_reference(article)
                graphdict5 = graph_extract_article_cited(article)

                l_nodes.extend(graphdict1["nodes"])
                l_nodes.extend(graphdict2["nodes"])
                l_nodes.extend(graphdict3["nodes"])
                l_nodes.extend(graphdict4["nodes"])
                l_nodes.extend(graphdict5["nodes"])

                l_edges.extend(graphdict1["edges"])
                l_edges.extend(graphdict2["edges"])
                l_edges.extend(graphdict3["edges"])
                l_edges.extend(graphdict4["edges"])
                l_edges.extend(graphdict5["edges"])

                bar.label = f"Article ({n}): Total ({len(l_nodes)},{len(l_edges)})"
                # logger.DEBUG(f'Article ({n}): Extract {len(a_nodes)} Nodes & {len(a_edges)} Edges. Total ({len(l_nodes)},{len(l_edges)})')
    if remove_duplicate:
        print()
        logger.DEBUG("Remove duplication in Nodes & Edges. ")
        n = Emmanuel(l_nodes)
        e = Emmanuel(l_edges)
        logger.DEBUG(f"Final {len(n)} Nodes & {len(e)} Edges Extracted.")
        return {"nodes": n, "edges": e}
    else:
        return {"nodes": l_nodes, "edges": l_edges}


def check_upper_term(n: dict, text: str):
    """
    It takes a node and a string as input, and if the node's name contains the string, it returns a new
    node and edge that connects the new node to the input node.

    The new node is a "UpperTopic" node, and the new edge is an "IS_A" edge.

    The function returns a dictionary with two keys: "node" and "edge".


    :param n: the node we're checking
    :type n: dict
    :param text: The text to be checked
    :type text: str
    :return: A dictionary with two keys, 'node' and 'edge'. The values of these keys are dictionaries.
    """

    if n["Name"].__contains__(text.lower()):
        new_node = {
            "Name": text.upper(),
            "Type": "UpperTopic",
            "Identifier": text.upper(),
        }
        new_edge = {
            "SourceID": n["Identifier"],
            "DestinationID": new_node["Identifier"],
            "Type": "IS_A",
            "HashID": str(hash(n["Identifier"] + new_node["Identifier"] + "IS_A")),
        }

        return {"node": new_node, "edge": new_edge}
    else:
        return None


if __name__ == "__main__":
    pass
    # f = open(r"C:\Users\Bitaraf\Desktop\New folder\temp-with-duplication.json")
    # data = json.load(f)
    # f.close()
    # print("load complete.")
    # l_nodes = data["nodes"]
    # l_edges = data["edges"]
    # n = thefourtheye_2(l_nodes)
    # print("node complete.")
    # e = thefourtheye_2(l_edges)
    # print("edge complete.")

    # graphdict = {"nodes": l_nodes, "edges": l_edges}
    # data= json.dumps(graphdict, indent=4)
    # with open("bcancer-all.json", "w") as outfile:
    #     outfile.write(data)
