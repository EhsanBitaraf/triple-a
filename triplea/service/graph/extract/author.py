from triplea.schemas.article import Article
from triplea.schemas.node import Edge, Node


def graph_extract_article_author_affiliation(article: Article) -> dict:
    """
    It takes an article object and returns a dictionary with two keys:
     nodes and edges. The nodes key
    contains a list of nodes and the edges key contains a list of edges.

    :param article: Article - This is the article object
      that we created earlier
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

    if article.Authors is not None:
        for author in article.Authors:
            node_author = Node()
            node_author.Identifier = author.HashID
            node_author.Name = author.FullName
            node_author.Type = "Author"
            nodes.append(node_author.dict())

            edge = Edge()
            edge.SourceID = node_author.Identifier
            edge.DestinationID = node_article.Identifier
            edge.Type = "AUTHOR_OF"
            edge.HashID = str(hash(edge.SourceID + edge.DestinationID + edge.Type))
            edges.append(edge.dict())

            # Creating a graph of authors and affiliation.
            if author.Affiliations is not None:
                for aff in author.Affiliations:
                    node_affiliation = Node()
                    node_affiliation.Identifier = aff.HashID
                    node_affiliation.Name = aff.Part1
                    node_affiliation.Type = "Affiliation"
                    nodes.append(node_affiliation.dict())

                    edge = Edge()
                    edge.SourceID = node_author.Identifier
                    edge.DestinationID = node_affiliation.Identifier
                    edge.Type = "IS_MEMBER_OF"
                    edge.HashID = str(
                        hash(edge.SourceID + edge.DestinationID + edge.Type)
                    )
                    edges.append(edge.dict())

    return {"nodes": nodes, "edges": edges}
