import json
from pymongo import MongoClient


from triplea.db.database import DataBase
from triplea.config.settings import SETTINGS
from triplea.schemas.article import Article

class DB_MongoDB(DataBase):
    _connection_url = SETTINGS.AAA_MONGODB_CONNECTION_URL
    client = MongoClient(_connection_url)
    db = client[SETTINGS.AAA_MONGODB_DB_NAME]
    col_article = db["articledata"]
    col_nodes = db["nodes"]
    col_edges = db["edges"]

    def add_new_article(self, article:Article) -> int:
        article_json = json.loads(json.dumps(article, default=lambda o: o.__dict__, sort_keys=True, indent=4))
        result = self.col_article.insert_one(article_json)
        return result.inserted_id

    def get_article_by_state(self,state:int):
        myquery = { "State":  state}
        cursor = self.col_article.find(myquery)
        if len(list(cursor.clone())) == 0 :
            return None
        else:
            return list(cursor)

    def get_article_by_pmid(self,pmid:str):
        myquery = { "PMID":  pmid}
        cursor = self.col_article.find(myquery)
        # r = self.col_article.find_one()
        
        if len(list(cursor.clone())) == 0 :
            return None
        else:
            la = list(cursor)
            return la
            # la = []
            # for d in cursor:
            #     print(type(d))
            #     la.append(d)
            #     return la

  


    def get_all_article_count(self)-> int:
        """
        > This function returns the number of articles in the database
        :return: The length of the database.
        """
        return self.col_article.count_documents({})

    def is_article_exist_by_pmid(self,pmid:str) -> bool:
        """
        > Check if the article with the given PMID exists in the database
        
        :param pmid: the PMID of the article
        :type pmid: str
        :return: A boolean value.
        """
        myquery = { "PMID":  pmid}
        if self.col_article.count_documents(myquery) > 0:
            return True
        else:
            return False
        