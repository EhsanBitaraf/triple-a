import os
from triplea.db.database import DataBase
import json
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware

from triplea.schemas.article import Article
from triplea.schemas.node import Edge, Node

from triplea.config.settings import DB_ROOT_PATH
from triplea.config.settings import SETTINGS
from triplea.utils.general import JSONEncoder


class DB_TinyDB(DataBase):
    # db = TinyDB(DB_ROOT_PATH / 'articledata.json')
    if SETTINGS.AAA_DB_TYPE == "TinyDB":
        if not os.path.exists(DB_ROOT_PATH):
            os.makedirs(DB_ROOT_PATH)

        db = TinyDB(
            os.path.join(DB_ROOT_PATH, SETTINGS.AAA_TINYDB_FILENAME),
            storage=CachingMiddleware(JSONStorage),
        )
    else:
        db = []

    def add_new_article(self, article: Article) -> int:
        article_json = json.loads(
            # json.dumps(article, default=lambda o: o.__dict__, sort_keys=True, indent=4)
            json.dumps(article, cls=JSONEncoder, sort_keys=True, indent=4)
        )
        # article_json = json.dumps(article.json())
        return self.db.insert(article_json)

    def get_article_by_state(self, state: int):
        q = Query()
        return self.db.search(q.State == state)

    def get_article_pmid_list_by_state(self, state: int):
        q = Query()
        l_pmid = [a.get("PMID") for a in self.db.search(q.State == state)]
        return l_pmid

    def get_article_id_list_by_state(self, state: int):
        q = Query()
        l_pmid = [a.doc_id for a in self.db.search(q.State == state)]
        return l_pmid

    def get_article_pmid_list_by_cstate(self, state: int, tag_field: str):
        q = Query()
        if state is None or state == 0:
            # query = (Query().FlagAffiliationMining == 0)
            # | (Query().FlagAffiliationMining == None)
            # | (~Query().FlagAffiliationMining.exists())
            query = (
                (Query()[tag_field] == 0)
                | (Query()[tag_field] == None)  # noqa: E711
                | (~Query()[tag_field].exists())
            )  # noqa: E501,E711
            l_pmid = [a.get("PMID") for a in self.db.search(query)]
        else:
            l_pmid = [a.get("PMID") for a in self.db.search(q[tag_field] == state)]
        return l_pmid

    def get_article_id_list_by_cstate(self, state: int, tag_field: str):
        q = Query()
        if state is None or state == 0:
            # is None = raise exception
            query = (
                (Query()[tag_field] == 0)
                | (Query()[tag_field] == None)  # noqa: E711
                | (~Query()[tag_field].exists())
            )  # noqa: E711,E501
            l_id = [a.doc_id for a in self.db.search(query)]
        else:
            l_id = [a.doc_id for a in self.db.search(q[tag_field] == state)]
        return l_id

    def get_all_article_pmid_list(self):
        l_all = self.db.all()
        l_pmid = []
        for i in l_all:
            l_pmid.append(i["PMID"])
        return l_pmid

    def get_all_article_id_list(self):
        l_all = self.db.all()
        l_id = []
        for i in l_all:
            l_id.append(i.doc_id)
        return l_id

    def get_count_article_by_state(self, state: int):
        q = Query()
        l_pmid = self.db.search(q.State == state)
        return len(l_pmid)

    def get_article_by_arxiv_id(self, arxiv_id: str):
        q = Query()
        return self.db.get(q.ArxivID == arxiv_id)

    def get_article_by_pmid(self, pmid: str):
        q = Query()
        return self.db.get(q.PMID == pmid)

    def get_article_by_id(self, id: str):
        return self.db.get(doc_id=id)

    def update_article_by_pmid(self, article: Article, pmid: str):
        article_json = json.loads(
            # json.dumps(article, default=lambda o: o.__dict__, sort_keys=True, indent=4)
            json.dumps(article, cls=JSONEncoder, sort_keys=True, indent=4)
        )
        q = Query()
        return self.db.update(article_json, q.PMID == pmid)

    def update_article_by_id(self, article: Article, id: str):
        article_json = json.loads(
            json.dumps(article, cls=JSONEncoder, sort_keys=True, indent=4)
        )

        return self.db.update(article_json, doc_ids=[id])

    def update_cstate_by_id(id, tag_field: str, new_state: int):
        raise NotImplementedError

    def is_article_exist_by_pmid(self, pmid: str) -> bool:
        """
        > Check if the article with the given PMID exists in the database

        :param pmid: the PMID of the article
        :type pmid: str
        :return: A boolean value.
        """
        q = Query()
        return self.db.contains(q.PMID == pmid)

    def is_article_exist_by_arxiv_id(self, id: str) -> bool:
        q = Query()
        return self.db.contains(q.ArxivID == id)

    def get_all_article_count(self) -> int:
        """
        > This function returns the number of articles in the database
        :return: The length of the database.
        """
        return len(self.db)

    # region Extra Article Method

    def change_flag_extract_topic(self, current_value, set_value):
        # Update the value of "FlagExtractTopic" from 0 to 1
        return self.db.update(
            {"FlagExtractTopic": set_value}, Query().FlagExtractTopic == current_value
        )

    # endregion

    # region Node

    def add_new_node(self, node: Node) -> int:
        node_json = json.loads(
            json.dumps(node, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        )
        table = self.db.table("node")
        return table.insert(node_json)

    def is_node_exist_by_identifier(self, identifier: str) -> bool:
        table = self.db.table("node")
        q = Query()
        return table.contains(q.Identifier == identifier)

    def get_all_node_count(self) -> int:
        table = self.db.table("node")
        return len(table)

    def get_all_nodes(self):
        table = self.db.table("node")
        return table.all()

    # endregion

    # region Edge

    def add_new_edge(self, edge: Edge) -> int:
        edge_json = json.loads(
            json.dumps(edge, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        )
        table = self.db.table("edge")
        return table.insert(edge_json)

    def is_edge_exist_by_hashid(self, hashid: str) -> bool:
        table = self.db.table("edge")
        q = Query()
        return table.contains(q.HashID == hashid)

    def get_all_edge_count(self) -> int:
        table = self.db.table("edge")
        return len(table)

    def get_all_edges(self):
        table = self.db.table("edge")
        return table.all()

    # endregion

    # region Triple
    def add_new_triple(self, edge: dict) -> int:
        # triple_json = json.loads(
        #     json.dumps(edge, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        # )
        table = self.db.table("triple")
        triple_json = edge
        return table.insert(triple_json)

    # endregion

    def close(self):
        self.db.close()

    def flush(self):
        self.db.storage.flush()

    def refresh(self):
        self.db.close()
        self.db = TinyDB(
            os.path.join(DB_ROOT_PATH, SETTINGS.AAA_TINYDB_FILENAME),
            storage=CachingMiddleware(JSONStorage),
        )

    def get_article_group_by_state(self):
        r = []
        for i in range(-4, 7):
            n = 0
            q = Query()
            n = self.db.count(q.State == i)
            r.append({"State": i, "n": n})

        return r
