

import sys
import time

import click
from typing import Optional
from triplea.schemas.article import Article
from triplea.schemas.node import Edge, Node
import triplea.service.repository.persist as persist
from triplea.service.click_logger import logger

from triplea.service.graph.extract.topic import graph_extract_article_topic 
from triplea.service.graph.extract.author import graph_extract_article_author_affiliation
from triplea.service.graph.extract.keyword import graph_extract_article_keyword
from triplea.service.graph.extract.reference import graph_extract_article_reference
from triplea.service.graph.extract.cited import graph_extract_article_cited
__all__ = ["graph_extractor", 
           "graph_extract_article_topic",
           "graph_extract_article_author_affiliation",
           "graph_extract_article_keyword",
           "graph_extract_article_reference",
           "graph_extract_article_cited"
           ]
 
def Emmanuel(d:list)->list:
    """Base on [this](https://stackoverflow.com/questions/9427163/remove-duplicate-dict-in-list-in-python)

    Args:
        d (list): _description_

    Returns:
        list: _description_
    """
    return [i for n, i in enumerate(d) if i not in d[n + 1:]]

def thefourtheye_2(data):
    """
    It takes a list of dictionaries, converts each dictionary to a frozenset of tuples, and then uses
    the frozenset as a key in a dictionary, with the value being the original dictionary
    Base on [this](https://stackoverflow.com/questions/9427163/remove-duplicate-dict-in-list-in-python)

    :param data: The list of dictionaries that you want to remove duplicates from
    :return: A dictionary with the keys being the frozenset of the items in the list and the values
    being the items in the list.
    """
    return {frozenset(item.items()):item for item in data}.values()

def graph_extractor(func , state:int, limit_node: Optional[int] = 0):
    """
    It takes a function as an argument, and returns a dictionary of nodes and edges
    
    :param func: the function that will be used to extract the graph from the article
    :param state: the state of the article, which is an integer
    :type state: int
    :return: A dictionary with two keys, 'nodes' and 'edges'. The values are remove duplicate nodes & edge with Emmanuel algoritm.
    """
    l_pmid = persist.get_article_pmid_list_by_state(state)
    logger.INFO(str(len(l_pmid)) + ' Article(s) is in state ' + str(state))
    l_nodes=[]
    l_edges = []
    n  = 0
    with click.progressbar(length=len(l_pmid), show_pos=True,show_percent =True) as bar:
        for id in l_pmid:
            n = n + 1
            bar.update(1)
            a = persist.get_article_by_pmid(id)
            try:
                article = Article(**a.copy())
            except:
                exc_type, exc_value, exc_tb = sys.exc_info()
                print()
                logger.ERROR(f'Error {exc_type}')
                logger.ERROR(f'Error {exc_value}')
                # logger.ERROR(f'Error {exc_tb.tb_next}')
                article = None

 
            if limit_node != 0 : # Unlimited
                if n == limit_node:
                    logger.DEBUG(f'Remove duplication in Nodes & Edges. ')
                    n = Emmanuel(l_nodes)
                    e = Emmanuel(l_edges)
                    logger.DEBUG(f'Final {len(n)} Nodes & {len(e)} Edges Extracted.')
                    return { 'nodes' : n , 'edges' : e}

            if article is not None:
                # data = _extract_article_topic(article)
                data = func(article)
                a_nodes = data['nodes']
                a_edges = data['edges']
                l_nodes.extend(a_nodes)
                l_edges.extend(a_edges)
                bar.label = f'Article ({n}): Extract {len(a_nodes)} Nodes & {len(a_edges)} Edges. Total ({len(l_nodes)},{len(l_edges)})'
                # logger.DEBUG(f'Article ({n}): Extract {len(a_nodes)} Nodes & {len(a_edges)} Edges. Total ({len(l_nodes)},{len(l_edges)})')

    print()
    logger.DEBUG(f'Remove duplication in Nodes & Edges. ')
    n = Emmanuel(l_nodes)
    e = Emmanuel(l_edges)
    logger.DEBUG(f'Final {len(n)} Nodes & {len(e)} Edges Extracted.')
    return { 'nodes' : n , 'edges' : e}



def graph_extractor_all_entity( state:int, limit_node: Optional[int] = 0):
    l_pmid = persist.get_article_pmid_list_by_state(state)
    logger.INFO(str(len(l_pmid)) + ' Article(s) is in state ' + str(state))
    l_nodes=[]
    l_edges = []
    n  = 0
    with click.progressbar(length=len(l_pmid), show_pos=True,show_percent =True) as bar:
        for id in l_pmid:
            n = n + 1
            bar.update(1)
            a = persist.get_article_by_pmid(id)
            try:
                article = Article(**a.copy())
            except:
                exc_type, exc_value, exc_tb = sys.exc_info()
                print()
                logger.ERROR(f'Error {exc_type}')
                logger.ERROR(f'Error {exc_value}')
                # logger.ERROR(f'Error {exc_tb.tb_next}')
                article = None

 
            if limit_node != 0 : # Unlimited
                if n == limit_node:
                    logger.DEBUG(f'Remove duplication in Nodes & Edges. ')
                    n = Emmanuel(l_nodes)
                    e = Emmanuel(l_edges)
                    logger.DEBUG(f'Final {len(n)} Nodes & {len(e)} Edges Extracted.')
                    return { 'nodes' : n , 'edges' : e}

            if article is not None:
                # data = _extract_article_topic(article)


                graphdict1 = graph_extract_article_author_affiliation(article)
                graphdict2 = graph_extract_article_topic(article)
                graphdict3 = graph_extract_article_keyword(article)
                graphdict4 = graph_extract_article_reference(article)
                # graphdict5 = graph_extract_article_cited(article)
     
                l_nodes.extend(graphdict1['nodes'])
                l_nodes.extend(graphdict2['nodes'])
                l_nodes.extend(graphdict3['nodes'])
                l_nodes.extend(graphdict4['nodes'])
                # nodes.extend(graphdict5['nodes'])

                l_edges.extend(graphdict1['edges'])
                l_edges.extend(graphdict2['edges'])
                l_edges.extend(graphdict3['edges'])
                l_edges.extend(graphdict4['edges'])
                # edges.extend(graphdict5['edges'])

                bar.label = f'Article ({n}): Total ({len(l_nodes)},{len(l_edges)})'
                # logger.DEBUG(f'Article ({n}): Extract {len(a_nodes)} Nodes & {len(a_edges)} Edges. Total ({len(l_nodes)},{len(l_edges)})')

    print()
    logger.DEBUG(f'Remove duplication in Nodes & Edges. ')
    n = Emmanuel(l_nodes)
    e = Emmanuel(l_edges)
    logger.DEBUG(f'Final {len(n)} Nodes & {len(e)} Edges Extracted.')
    return { 'nodes' : n , 'edges' : e}


def check_upper_term(n:dict,text:str):
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

    if n['Name'].__contains__(text.lower()):
        new_node = {'Name' : text.upper() , 'Type' : 'UpperTopic' , 'Identifier' : text.upper()}
        new_edge = {'SourceID' : n['Identifier'] ,
                        'DestinationID' : new_node['Identifier'],
                        'Type' : 'IS_A',
                        'HashID' : str(hash(n['Identifier'] + new_node['Identifier'] + 'IS_A'))
                        } 

        return {'node' : new_node , 'edge' : new_edge} 
    else:
        return None     

if __name__ == '__main__':
    pass
    