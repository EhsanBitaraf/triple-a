import json
from pymongo import MongoClient


from triplea.db.database import DataBase
from triplea.config.settings import SETTINGS
from triplea.schemas.article import Article
from triplea.schemas.node import Edge, Node


class DB_MongoDB(DataBase):
    _connection_url = SETTINGS.AAA_MONGODB_CONNECTION_URL
    client = MongoClient(_connection_url)
    db = client[SETTINGS.AAA_MONGODB_DB_NAME]
    col_article = db["articledata"]
    col_nodes = db["nodes"]
    col_edges = db["edges"]
    col_triple = db["triple"]

    # region Article

    def add_new_article(self, article: Article) -> int:
        article_json = json.loads(
            json.dumps(article, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        )
        result = self.col_article.insert_one(article_json)
        return result.inserted_id

    def get_article_by_state(self, state: int):
        myquery = {"State": state}
        cursor = self.col_article.find(myquery)
        la = list(cursor)
        if len(la) == 0:
            return None
        else:
            return la

    def get_article_pmid_list_by_state(self, state: int):
        myquery = {"State": state}
        cursor = self.col_article.find(myquery, projection={"PMID": "$PMID", "_id": 0})

        la = list(cursor)
        new_la = []
        for c in la:
            new_la.append(c["PMID"])

        if len(new_la) == 0:
            return []
        else:
            return new_la

    def get_article_pmid_list_by_cstate(self, state: int, tag_field: str):
        if state is None or state == 0:
            myquery = {"$or": [{tag_field: None}, {tag_field: 0}]}
        else:
            myquery = {tag_field: state}

        cursor = self.col_article.find(myquery, projection={"PMID": "$PMID", "_id": 0})

        la = list(cursor)
        new_la = []
        for c in la:
            new_la.append(c["PMID"])

        if len(new_la) == 0:
            return []
        else:
            return new_la

    def get_all_article_pmid_list(self):
        myquery = {}
        cursor = self.col_article.find(myquery, projection={"PMID": "$PMID", "_id": 0})

        la = list(cursor)
        new_la = []
        for c in la:
            new_la.append(c["PMID"])

        if len(new_la) == 0:
            return []
        else:
            return new_la

    def get_count_article_by_state(self, state: int):
        myquery = {"State": state}
        return self.col_article.count_documents(myquery)

    def get_article_by_pmid(self, pmid: str):
        myquery = {"PMID": pmid}
        cursor = self.col_article.find(myquery)
        # r = self.col_article.find_one()

        if len(list(cursor.clone())) == 0:
            return None
        else:
            la = list(cursor)
            return la[0]
            # la = []
            # for d in cursor:
            #     print(type(d))
            #     la.append(d)
            #     return la

    def update_article_by_pmid(self, article: Article, pmid: str):
        article_json = json.loads(
            json.dumps(article, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        )
        myquery = {"PMID": pmid}
        r = self.col_article.replace_one(myquery, article_json)
        return r.raw_result

    def is_article_exist_by_pmid(self, pmid: str) -> bool:
        """
        > Check if the article with the given PMID exists in the database

        :param pmid: the PMID of the article
        :type pmid: str
        :return: A boolean value.
        """
        myquery = {"PMID": pmid}
        if self.col_article.count_documents(myquery) > 0:
            return True
        else:
            return False

    def get_all_article_count(self) -> int:
        """
        > This function returns the number of articles in the database
        :return: The length of the database.
        """
        return self.col_article.count_documents({})

    def get_article_group_by_state(self):
        pipeline = [
            {"$group": {"_id": {"State": "$State"}, "COUNT(_id)": {"$sum": 1}}},
            {"$project": {"State": "$_id.State", "n": "$COUNT(_id)", "_id": 0}},
        ]
        return list(self.col_article.aggregate(pipeline))

    # region Extra Article Method

    def change_flag_extract_topic(self, current_value, set_value):
        myquery = {"FlagExtractTopic": current_value}
        sett = {"$set": {"FlagExtractTopic": set_value}}
        r = self.col_article.update_many(myquery, sett)
        return r

    # endregion

    # endregion

    # region Node

    def add_new_node(self, node: Node) -> int:
        node_json = json.loads(
            json.dumps(node, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        )
        result = self.col_nodes.insert_one(node_json)
        return result.inserted_id

    def is_node_exist_by_identifier(self, identifier: str) -> bool:
        myquery = {"Identifier": identifier}
        if self.col_nodes.count_documents(myquery) > 0:
            return True
        else:
            return False

    def get_all_node_count(self) -> int:
        return self.col_nodes.count_documents({})

    def get_all_nodes(self):
        raise NotImplementedError

    # endregion

    # region Edge

    def add_new_edge(self, edge: Edge) -> int:
        edge_json = json.loads(
            json.dumps(edge, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        )
        result = self.col_edges.insert_one(edge_json)
        return result.inserted_id

    def is_edge_exist_by_hashid(self, hashid: str) -> bool:
        myquery = {"HashID": hashid}
        if self.col_edges.count_documents(myquery) > 0:
            return True
        else:
            return False

    def get_all_edge_count(self) -> int:
        return self.col_edges.count_documents({})

    def get_all_edges(self):
        raise NotImplementedError

    # endregion

    # region Triple
    def add_new_triple(self, edge: dict) -> int:
        triple_json = json.loads(
            json.dumps(edge, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        )
        result = self.col_triple.insert_one(triple_json)
        return result.inserted_id

    # endregion

    def close(self):
        self.client.close

    def flush(self):
        pass

    def refresh(self):
        pass


if __name__ == "__main__":
    db = DB_MongoDB()
    # print(list(db.get_article_group_by_state()))
    print(db.get_article_pmid_list_by_state(-1))
