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
        return db.search(q.state == None)



if SETTINGS.DB_TYPE == 'TinyDB':
    db = DB_TinyDB()
else:
    raise NotImplemented