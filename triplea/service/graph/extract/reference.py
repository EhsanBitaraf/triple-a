from triplea.schemas.article import Article
from triplea.schemas.node import Edge, Node

def graph_extract_article_reference(article: Article)-> dict: 
    nodes = []
    edges = []

    node_article = Node()
    node_article.Identifier = article.PMID
    node_article.Name = article.PMID
    node_article.Type = 'Article'
    nodes.append(node_article.dict())

    if article.References is not None:
        for ref in article.References:
            node_reference = Node()
            node_reference.Identifier = ref
            node_reference.Name = ref
            node_reference.Type = 'Article'
            nodes.append(node_reference.dict())

            edge = Edge()
            edge.SourceID = node_article.Identifier
            edge.DestinationID = node_reference.Identifier
            edge.Type = 'REFERENCE'
            edge.HashID =  str(hash(edge.SourceID + edge.DestinationID + edge.Type ))
            edges.append(edge.dict())

    return { 'nodes' : nodes, 'edges' : edges}