from typing import Optional
from triplea.db.dal import db
from triplea.schemas.article import Article
from triplea.schemas.node import Edge, Node


def create_article(article:Article):
    db.add_new_article(article)

def get_article_by_state(state:int):
    return db.get_article_by_state(state)

def get_article_by_pmid(pmid:str):
    return db.get_article_by_pmid(pmid)

def update_article_by_pmid(article,pmid:str):
    return db.update_article_by_pmid(article,pmid)

def insert_new_pmid(pmid:str ,
                    querytranslation: Optional[str] = None ):
    """
    If the article is not in the database, add it
    
    :param pmid: The PMID of the article you want to insert
    :type pmid: str
    :return: The return value is the ID of the newly inserted article.
    """
    # check PMID is exist
    if db.is_article_exist_by_pmid(pmid):
        pass
        return
    else: # Insert not exist Article
        a = Article(PMID = pmid , State= 0 , QueryTranslation = querytranslation)
        return db.add_new_article(a)



def get_all_article_count()-> int:
    """
    This function returns the number of articles in the knowledge repository
    :return: The number of articles in the knowledge repository.
    """
    return db.get_all_article_count()

def create_node(node:Node)->int:
    if db.is_node_exist_by_identifier(node.Identifier):
        pass
        return
    else:
        return db.add_new_node(node)

def get_all_node_count()-> int:
    return db.get_all_node_count()

def get_all_nodes():
    return db.get_all_nodes()

def create_edge(edge:Edge)->int:
    if db.is_edge_exist_by_hashid(edge.HashID):
        pass
        return
    else:
        return db.add_new_edge(edge)

def get_all_edge_count()-> int:
    return db.get_all_edge_count()

def get_all_edges():
    return db.get_all_edges()