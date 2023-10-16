# flake8: noqa

from pymongo import MongoClient
from triplea.config.settings import SETTINGS


def get_flag():
    _connection_url = SETTINGS.AAA_MONGODB_CONNECTION_URL
    client = MongoClient(_connection_url)
    db = client[SETTINGS.AAA_MONGODB_DB_NAME]
    col_article = db["articledata"]
    pipeline = [
        {"$group": {"_id": {"State": "$State"}, "COUNT(_id)": {"$sum": 1}}},
        {"$project": {"State": "$_id.State", "n": "$COUNT(_id)", "_id": 0}},
    ]
    pipeline = [
        {
            "$group": {
                "_id": {"FlagAffiliationMining": "$FlagAffiliationMining"},
                "COUNT(_id)": {"$sum": 1},
            }
        },
        {
            "$project": {
                "FlagAffiliationMining": "$_id.FlagAffiliationMining",
                "n": "$COUNT(_id)",
                "_id": 0,
            }
        },
    ]
    print(list(col_article.aggregate(pipeline)))


def change():
    _connection_url = SETTINGS.AAA_MONGODB_CONNECTION_URL
    client = MongoClient(_connection_url)
    db = client[SETTINGS.AAA_MONGODB_DB_NAME]
    col_article = db["articledata"]
    myquery = {"FlagAffiliationMining": 1}
    sett = {"$set": {"FlagAffiliationMining": 0}}
    r = col_article.update_many(myquery, sett)


def change_CiteCrawlerDeep():
    _connection_url = SETTINGS.AAA_MONGODB_CONNECTION_URL
    client = MongoClient(_connection_url)
    db = client[SETTINGS.AAA_MONGODB_DB_NAME]
    col_article = db["articledata"]
    # col_nodes = db["nodes"]
    # col_edges = db["edges"]
    # col_triple = db["triple"]
    myquery = {"CiteCrawlerDeep": 0}
    sett = {"$set": {"CiteCrawlerDeep": 1}}
    r = col_article.update_many(myquery, sett)


def change_State():
    _connection_url = SETTINGS.AAA_MONGODB_CONNECTION_URL
    client = MongoClient(_connection_url)
    db = client[SETTINGS.AAA_MONGODB_DB_NAME]
    col_article = db["articledata"]
    myquery = {"State": 3}
    sett = {"$set": {"State": 2}}
    r = col_article.update_many(myquery, sett)


def change_complex():
    _connection_url = SETTINGS.AAA_MONGODB_CONNECTION_URL
    client = MongoClient(_connection_url)
    db = client[SETTINGS.AAA_MONGODB_DB_NAME]
    col_article = db["articledata"]
    # myquery = {"FlagAffiliationMining": 1}
    # sett = {"$set": {"FlagAffiliationMining": 0}}
    # r = col_article.update_many(myquery, sett)

    myquery = {"FlagAffiliationMining": 0, "Authors.Affiliations": {"$ne": "null"}}
    sett = {"$unset": {"Authors.$[author].Affiliations.$[affil].Structural": ""}}
    filter = [
        {"author.Affiliations": {"$exists": True}},
        {"affil.Structural": {"$exists": True}},
    ]

    r = col_article.update_many(myquery, sett, array_filters=filter)


if __name__ == "__main__":
    pass
    # change()
    change_State()
