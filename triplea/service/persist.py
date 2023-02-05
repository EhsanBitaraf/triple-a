from triplea.db.dal import db
from triplea.schemas.article import Article


def create_article(article:Article):
    db.add_new_article(article)