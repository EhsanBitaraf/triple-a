from typing import Optional
from triplea.db.dal import db
from triplea.schemas.article import Article


def create_article(article:Article):
    db.add_new_article(article)

def get_article_by_state(state:int):
    return db.get_article_by_state(state)

def update_article_by_pmid(article,pmid:str):
    return db.update_article_by_pmid(article,pmid)

def insert_new_pmid(pmid:str ,
                    querytranslation: Optional[str] = None ):
    """
    If the article is not in the database, add it
    
    :param pmid: The PMID of the article you want to insert
    :type pmid: str
    :return: The return value is the ID of the newly inserted article.
    """
    # check PMID is exist
    if db.is_article_exist_by_pmid(pmid):
        pass
        return
    else: # Insert not exist Article
        a = Article(PMID = pmid , State= 0 , QueryTranslation = querytranslation)
        return db.add_new_article(a)

def get_all_article_count()-> int:
    """
    This function returns the number of articles in the knowledge repository
    :return: The number of articles in the knowledge repository.
    """
    return db.get_all_article_count()