import json
from tinydb import TinyDB, Query
from triplea.config.settings import SETTINGS,DB_ROOT_PATH
from triplea.schemas.article import Article



class DataBase():
    pass

class DB_TinyDB(DataBase):
    db = TinyDB(DB_ROOT_PATH / 'articledata.json')

    def add_new_article(self, article:Article) -> int:
        article_json = json.loads(json.dumps(article, default=lambda o: o.__dict__, sort_keys=True, indent=4))
        # article_json = json.dumps(article.json())
        return self.db.insert(article_json)
    
    def get_article_by_state(self,state:int):
        q = Query()
        
        return self.db.search(q.Title == None)
    
    def update_article_by_pmid(self,article, pmid:str):
        q = Query()
        return self.db.update(article , q.PMID == pmid)
    
    def is_article_exist_by_pmid(self,pmid:str) -> bool:
        """
        > Check if the article with the given PMID exists in the database
        
        :param pmid: the PMID of the article
        :type pmid: str
        :return: A boolean value.
        """
        q = Query()
        return self.db.contains(q.PMID == pmid)
    
    def get_all_article_count(self)-> int:
        """
        > This function returns the number of articles in the database
        :return: The length of the database.
        """
        return len(self.db)

if SETTINGS.DB_TYPE == 'TinyDB':
    db = DB_TinyDB()
else:
    raise NotImplemented






if __name__ == '__main__':
    ddb = DB_TinyDB()
    a = ddb.is_article_exist_by_pmid('3670594')
   
    print(a)