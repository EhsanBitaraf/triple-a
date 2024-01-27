from triplea.schemas.article import Article
from triplea.client.scigenius import article_embedding
import triplea.service.repository.persist as persist


def scigenius_article_embedding(article: Article, article_id):
    article.FlagEmbedding = 1
    if article.Abstract is not None:
        r = article_embedding(article)


    return article