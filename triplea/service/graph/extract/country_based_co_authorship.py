from triplea.schemas.article import Article
from triplea.schemas.node import Edge, Node

# from triplea.service.graph.extract import Emmanuel
from triplea.service.repository.state.custom.affiliation_mining import (
    get_structured_affiliation,
)


def graph_extract_article_country(article: Article) -> dict:
    nodes = []
    edges = []
    node_article = Node()
    node_article.Identifier = article.PMID
    node_article.Name = article.PMID
    node_article.Type = "Article"
    nodes.append(node_article.dict())

    affiliation_list = get_structured_affiliation(article)

    # affiliation_list = Emmanuel(affiliation_list)
    affiliation_list = [
        i for n, i in enumerate(affiliation_list) if i not in affiliation_list[n + 1:]
    ]

    for af in affiliation_list:
        if "country" in af:
            node_country = Node()
            node_country.Identifier = af["country"]
            node_country.Name = af["country"]
            node_country.Type = "Country"
            nodes.append(node_country.dict())

            edge = Edge()
            edge.SourceID = node_article.Identifier
            edge.DestinationID = node_country.Identifier
            edge.Type = "IS"
            edge.HashID = str(hash(edge.SourceID + edge.DestinationID + edge.Type))
            edges.append(edge.dict())

    return {"nodes": nodes, "edges": edges}
