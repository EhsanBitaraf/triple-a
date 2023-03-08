from triplea.schemas.article import Article
from triplea.schemas.node import Edge, Node


def graph_extract_article_cited(article: Article) -> dict:
    """
    > This function takes an article object and returns a dictionary with two keys: nodes and edges. relation between
    article and cited article

    :param article: Article - the article object that we want to extract the graph from
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

    if article.CitedBy is not None:
        for cite in article.CitedBy:
            node_cite = Node()
            node_cite.Identifier = cite
            node_cite.Name = cite
            node_cite.Type = "Article"
            nodes.append(node_cite.dict())

            edge = Edge()
            edge.SourceID = node_article.Identifier
            edge.DestinationID = node_cite.Identifier
            edge.Type = "CITED_BY"
            edge.HashID = str(hash(edge.SourceID + edge.DestinationID + edge.Type))
            edges.append(edge.dict())

    return {"nodes": nodes, "edges": edges}
