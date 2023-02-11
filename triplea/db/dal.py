import json
from tinydb import TinyDB, Query
from triplea.config.settings import SETTINGS,DB_ROOT_PATH
from triplea.schemas.article import Article
from triplea.schemas.node import Edge, Node

from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware

class DataBase():
    pass

class DB_TinyDB(DataBase):
    # db = TinyDB(DB_ROOT_PATH / 'articledata.json')
    db = TinyDB(DB_ROOT_PATH / 'articledata.json' , storage=CachingMiddleware(JSONStorage))
    

    def add_new_article(self, article:Article) -> int:
        article_json = json.loads(json.dumps(article, default=lambda o: o.__dict__, sort_keys=True, indent=4))
        # article_json = json.dumps(article.json())
        return self.db.insert(article_json)
    
    def get_article_by_state(self,state:int):
        q = Query()
        return self.db.search(q.State == state)

    def get_article_by_pmid(self,pmid:str):
        q = Query()
        return self.db.get(q.PMID == pmid)

    def update_article_by_pmid(self,article:Article, pmid:str):
        article_json = json.loads(json.dumps(article, default=lambda o: o.__dict__, sort_keys=True, indent=4))
        q = Query()
        return self.db.update(article_json , q.PMID == pmid)
    
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

    def add_new_node(self, node:Node)->int:
        node_json = json.loads(json.dumps(node, default=lambda o: o.__dict__, sort_keys=True, indent=4))
        table = self.db.table('node')
        return table.insert(node_json)

    def is_node_exist_by_identifier(self,identifier:str) -> bool:
        table = self.db.table('node')
        q = Query()
        return table.contains(q.Identifier == identifier)

    def get_all_node_count(self)-> int:
        table = self.db.table('node')
        return len(table)

    def get_all_nodes(self):
        table = self.db.table('node')
        return table.all()

    def add_new_edge(self, edge:Edge)->int:
        edge_json = json.loads(json.dumps(edge, default=lambda o: o.__dict__, sort_keys=True, indent=4))
        table = self.db.table('edge')
        return table.insert(edge_json)

    def is_edge_exist_by_hashid(self,hashid:str) -> bool:
        table = self.db.table('edge')
        q = Query()
        return table.contains(q.HashID == hashid)

    def get_all_edge_count(self)-> int:
        table = self.db.table('edge')
        return len(table)

    def get_all_edges(self):
        table = self.db.table('edge')
        return table.all()

    def close(self):
        self.db.close()

    def flush(self):
        self.db.storage.flush()

    def refresh(self):
        self.db.close()
        self.db = TinyDB(DB_ROOT_PATH / 'articledata.json' , storage=CachingMiddleware(JSONStorage))

if SETTINGS.DB_TYPE == 'TinyDB':
    db = DB_TinyDB()
else:
    raise NotImplemented






if __name__ == '__main__':
    ddb = DB_TinyDB()
    # a = ddb.is_article_exist_by_pmid('3670594')

    # ddb.db.drop_table('node')
    # ddb.db.drop_table('edge')
   
