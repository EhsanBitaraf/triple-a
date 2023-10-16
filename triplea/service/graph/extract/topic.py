from triplea.schemas.article import Article
from triplea.schemas.node import Edge, Node

# import spacy
# import pytextrank
from triplea.service.click_logger import logger

# nlp = spacy.load("en_core_web_sm")
# nlp.add_pipe("topicrank")


def graph_extract_article_topic(article: Article) -> dict:
    """
    > For each article, extract the top 10 topics from the title and create a node for each topic and an
    edge from the article to each topic

    :param article: Article - this is the article object that we will be extracting the topics from
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

    if article.Topics is not None:
        for t in article.Topics:
            node_topic = Node()
            node_topic.Identifier = t["text"].lower()
            node_topic.Name = t["text"].lower()
            node_topic.Type = "Topic"
            nodes.append(node_topic.dict())

            edge = Edge()
            edge.SourceID = node_article.Identifier
            edge.DestinationID = node_topic.Identifier
            edge.Type = "TOPIC"
            edge.Weight = t["rank"]
            edge.HashID = str(hash(edge.SourceID + edge.DestinationID + edge.Type))
            edges.append(edge.dict())
    else:
        logger.WARNING(f"Article Topics is empty. PMID : {article.PMID}")

    return {"nodes": nodes, "edges": edges}
