from typing import Optional
from triplea.db.dal import db
from triplea.schemas.article import Article
from triplea.schemas.node import Edge, Node
from triplea.service.click_logger import logger


# region Article


def create_article(article: Article):
    db.add_new_article(article)


def get_article_by_state(state: int):
    """
    This function returns a list of articles from the database that have a state that matches the state
    passed in as a parameter

    :param state: The state of the article
    :type state: int
    :return: A list of articles
    """
    return db.get_article_by_state(state)


def get_article_pmid_list_by_state(state: int):
    """
    This function returns a list of PubMed IDs (PMIDs) of articles that have a given state

    :param state: the state of the article, which is an integer
    :type state: int
    :return: A list of PMIDs
    """
    return db.get_article_pmid_list_by_state(state)


def get_article_pmid_list_by_cstate(state: int, tag_field: str):
    """
    This function returns a list of PubMed IDs (PMIDs) of articles that have a given custom state

    :param state: the state of the article, which is an integer
    :type state: int
    :return: A list of PMIDs
    """
    return db.get_article_pmid_list_by_cstate(state, tag_field)


def get_all_article_pmid_list():
    return db.get_all_article_pmid_list()


def get_count_article_by_state(state: int) -> int:
    """
    This function returns the number of articles in the database that have a given state

    :param state: int
    :type state: int
    :return: The number of articles in the database with the given state.
    """
    return db.get_count_article_by_state(state)


def get_article_by_pmid(pmid: str):
    """
    > This function takes a PubMed ID (pmid) as a string and returns the corresponding article from the
    database

    :param pmid: the PubMed ID of the article you want to retrieve
    :type pmid: str
    :return: Article dict.
    """
    return db.get_article_by_pmid(pmid)


def update_article_by_pmid(article, pmid: str):
    """
    This function updates an article in the database by its pmid

    :param article: a dictionary with the following keys:
    :param pmid: the pubmed id of the article
    :type pmid: str
    :return: ??
    """
    return db.update_article_by_pmid(article, pmid)


def insert_new_pmid(
    pmid: str,
    querytranslation: Optional[str] = None,
    insert_type: Optional[str] = None,
    reference_crawler_deep: Optional[int] = 0,
    cite_crawler_deep: Optional[int] = 0,
):
    """
    If the article is not in the database, add it

    :param pmid: The PMID of the article you want to insert
    :type pmid: str
    :return: The return value is the ID of the newly inserted article.
    """
    # check PMID is exist
    if db.is_article_exist_by_pmid(pmid):
        logger.DEBUG("The article " + pmid + " already exists.", deep=3)
        return
    else:  # Insert not exist Article
        insert_type_list = []
        if insert_type is not None:
            insert_type_list.append(insert_type)

        # # old version
        # a = Article(PMID = pmid , State= 0 , QueryTranslation = querytranslation , InsertType= insert_type_list, ReferenceCrawlerDeep = reference_crawler_deep)
        # New version
        a = Article(
            PMID=pmid,
            State=0,
            QueryTranslation=querytranslation,
            ReferenceCrawlerDeep=reference_crawler_deep,
            CiteCrawlerDeep=cite_crawler_deep,
        )

        return db.add_new_article(a)


def get_all_article_count() -> int:
    """
    This function returns the number of articles in the knowledge repository
    :return: The number of articles in the knowledge repository.
    """
    return db.get_all_article_count()


def get_article_group_by_state():
    """
    It returns a list of dictionaries, each dictionary containing the state name and the number of
    articles in that state
    :return: A list of tuples.
    """
    return db.get_article_group_by_state()


# region Extra Article Method


def change_flag_extract_topic(current_value, set_value):
    return db.change_flag_extract_topic(current_value, set_value)


# endregion


# endregion

# region Node


def create_node(node: Node) -> int:
    """
    It creates a node if it doesn't exist

    :param node: Node
    :type node: Node
    :return: Nothing.
    """
    if db.is_node_exist_by_identifier(node.Identifier):
        logger.DEBUG("Node " + node.Name + " is exist.", deep=3)
        return
    else:
        return db.add_new_node(node)


def get_all_node_count() -> int:
    """
    This function returns the number of nodes in the database
    :return: The number of nodes in the database.
    """
    return db.get_all_node_count()


def get_all_nodes():
    """
    It returns all nodes in the database
    :return: A list of all nodes in the database.
    """
    return db.get_all_nodes()


# endregion

# region Edge


def create_edge(edge: Edge) -> int:
    """
    > If the edge is not exist, add it to the database

    :param edge: Edge
    :type edge: Edge
    :return: The return value is the id of the edge in the database.
    """
    if db.is_edge_exist_by_hashid(edge.HashID):
        logger.DEBUG("Edge " + edge.HashID + " is exist.", deep=3)
        return
    else:
        return db.add_new_edge(edge)

    """
    It returns the number of edges in the graph.
    :return: The number of edges in the graph.
    """


def get_all_edge_count() -> int:
    """
    This function returns the number of edges in the graph
    :return: The number of edges in the graph.
    """
    return db.get_all_edge_count()


def get_all_edges():
    """
    > This function returns all edges in the graph
    :return: A list of all edges in the database.
    """
    return db.get_all_edges()


# endregion

# region Triple


def create_triple(triple: dict) -> int:
    # Duplication is not checked in this method,
    # and if it is ever checked, its place is here

    return db.add_new_triple(triple)


# endregion


def refresh():
    """
    It refreshes the database by calling the refresh() function from the database module.
      This function is important to TinyDB.
    """
    db.refresh()
