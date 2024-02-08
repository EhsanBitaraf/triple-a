from triplea.schemas.article import Article
from triplea.client.scigenius import article_embedding


def scigenius_article_embedding(article: Article, article_id):
    article.FlagEmbedding = 1
    try:
        if article.Abstract is not None:
            r = article_embedding(article)
            if r is not True:
                print("Not True!!")
    except Exception:
        article.FlagEmbedding = -1

    return article
