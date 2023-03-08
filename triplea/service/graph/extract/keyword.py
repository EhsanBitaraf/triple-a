from triplea.schemas.article import Article
from triplea.schemas.node import Edge, Node
from triplea.service.click_logger import logger


def graph_extract_article_keyword(article: Article) -> dict:
    """
    > This function takes an article and returns a dictionary with two keys: nodes and edges. The nodes
    key contains a list of nodes, and the edges key contains a list of edges. nodes contain article & keyword

    :param article: Article - the article object that we want to extract the keywords from
    :type article: Article
    :return: A dictionary with two keys: nodes and edges.
    """
    nodes = []
    edges = []

    node_article = Node()
    node_article.Identifier = article.PMID
    node_article.Name = article.PMID
    node_article.Type = "Article"
    nodes.append(node_article.dict())

    if article.Keywords is None:
        logger.WARNING(f"The article has no keywords. PMID : {article.PMID}")
    else:
        for key in article.Keywords:
            node_keyword = Node()
            node_keyword.Identifier = key.Text
            node_keyword.Name = key.Text
            node_keyword.Type = "Keyword"
            nodes.append(node_keyword.dict())

            edge = Edge()
            edge.SourceID = node_article.Identifier
            edge.DestinationID = node_keyword.Identifier
            edge.Type = "KEYWORD"
            edge.HashID = str(hash(edge.SourceID + edge.DestinationID))
            edges.append(edge.dict())

    return {"nodes": nodes, "edges": edges}
