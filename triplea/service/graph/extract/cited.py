from triplea.schemas.article import Article
from triplea.schemas.node import Edge, Node

def graph_extract_article_cited(article: Article)-> dict: 
    nodes = []
    edges = []
    raise NotImplementedError