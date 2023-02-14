from triplea.schemas.article import Article
from triplea.schemas.node import Edge, Node

def graph_extract_article_keyword(article: Article)-> dict: 
    nodes = []
    edges = []
 
    node_article = Node()
    node_article.Identifier = article.PMID
    node_article.Name = article.PMID
    node_article.Type = 'Article'
    nodes.append(node_article.dict())

    for key in article.Keywords:
        node_keyword = Node()
        node_keyword.Identifier = key.Text
        node_keyword.Name = key.Text
        node_keyword.Type = 'Keyword'
        nodes.append(node_keyword.dict())

        edge = Edge()
        edge.SourceID = node_article.Identifier
        edge.DestinationID = node_keyword.Identifier
        edge.Type = 'KEYWORD'
        edge.HashID =  str(hash(edge.SourceID + edge.DestinationID))
        edges.append(edge.dict())
    
    return { 'nodes' : nodes, 'edges' : edges}