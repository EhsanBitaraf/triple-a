from triplea.schemas.article import Article
from triplea.schemas.node import Edge, Node
import spacy
import pytextrank

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("topicrank")

def _extract_article_topic(article: Article): 
    nodes = []
    edges = []

    node_article = Node()
    node_article.Identifier = article.PMID
    node_article.Name = article.PMID
    node_article.Type = 'Article'
    nodes.append(node_article.dict())

    doc = nlp(article.Title)

    for t in doc._.phrases[:10]:
        node_topic = Node()
        node_topic.Identifier = t.text.lower()
        node_topic.Name = t.text.lower()
        node_topic.Type = 'Topic'
        nodes.append(node_topic.dict())

        edge = Edge()
        edge.SourceID = node_article.Identifier
        edge.DestinationID = node_topic.Identifier
        edge.Type = 'TOPIC'
        edge.Weight = t.rank
        edge.HashID =  str(hash(edge.SourceID + edge.DestinationID + edge.Type))
        edges.append(edge.dict())

    return { 'nodes' : nodes, 'edges' : edges}

