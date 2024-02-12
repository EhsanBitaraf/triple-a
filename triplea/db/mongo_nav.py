from pymongo import MongoClient
from triplea.config.settings import SETTINGS


def get_database_list():
    _connection_url = SETTINGS.AAA_MONGODB_CONNECTION_URL
    client = MongoClient(_connection_url)
    dbs = client.list_database_names()
    return dbs


def get_article_title_and_abstract():
    _connection_url = SETTINGS.AAA_MONGODB_CONNECTION_URL
    client = MongoClient(_connection_url)
    db = client[SETTINGS.AAA_MONGODB_DB_NAME]
    col_article = db["articledata"]
    result = list(
        col_article.find(
            {"ArxivID": "1807.07455v2"}, {"_id": 0, "Title": 1, "Abstract": 1}
        )
    )
    return result


def get_article_info_with_llm_response(response: str):
    _connection_url = SETTINGS.AAA_MONGODB_CONNECTION_URL
    client = MongoClient(_connection_url)
    db = client[SETTINGS.AAA_MONGODB_DB_NAME]
    col_article = db["articledata"]
    result = list(
        col_article.find(
            {"ReviewLLM.Response": response, "ReviewLLM.TemplateID": "T101"},
            {"_id": 0, "PMID": 1, "ArxivID": 1, "Title": 1},
        )
    )
    return result


def get_groupby_with_llm_response():
    _connection_url = SETTINGS.AAA_MONGODB_CONNECTION_URL
    client = MongoClient(_connection_url)
    db = client[SETTINGS.AAA_MONGODB_DB_NAME]
    col_article = db["articledata"]
    pipeline = [
        {"$unwind": "$ReviewLLM"},
        {
            "$group": {
                "_id": "$ReviewLLM.Response",
                "count": {"$sum": 1},
                "totalInputTokens": {"$sum": "$ReviewLLM.InputTokens"},
                "totalOutputTokens": {"$sum": "$ReviewLLM.OutputTokens"},
                "totalTimeTaken": {"$sum": "$ReviewLLM.TimeTaken"},
            }
        },
    ]

    result = list(col_article.aggregate(pipeline))
    return result


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
    print(f"result: {r}")


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
    print(f"result: {r}")


def change_State():
    _connection_url = SETTINGS.AAA_MONGODB_CONNECTION_URL
    client = MongoClient(_connection_url)
    db = client[SETTINGS.AAA_MONGODB_DB_NAME]
    col_article = db["articledata"]
    myquery = {"State": 3}
    sett = {"$set": {"State": 2}}
    r = col_article.update_many(myquery, sett)
    print(f"result: {r}")


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
    print(f"result: {r}")


def change_reset_flag_llm_with_response(response: str, template_id: str):
    _connection_url = SETTINGS.AAA_MONGODB_CONNECTION_URL
    client = MongoClient(_connection_url)
    db = client[SETTINGS.AAA_MONGODB_DB_NAME]
    col_article = db["articledata"]

    myquery = {
        "FlagShortReviewByLLM": 1,
        "ReviewLLM.Response": response,
        "ReviewLLM.TemplateID": template_id,
    }
    update = {"$set": {"FlagShortReviewByLLM": 0, "ReviewLLM": None}}

    r = col_article.update_many(myquery, update)
    print(f"result: {r}")


def change_reset_flag_llm_with_template_id(template_id: str):
    _connection_url = SETTINGS.AAA_MONGODB_CONNECTION_URL
    client = MongoClient(_connection_url)
    db = client[SETTINGS.AAA_MONGODB_DB_NAME]
    col_article = db["articledata"]

    myquery = {"FlagShortReviewByLLM": 1, "ReviewLLM.TemplateID": template_id}
    update = {"$set": {"FlagShortReviewByLLM": 0, "ReviewLLM": None}}

    r = col_article.update_many(myquery, update)
    print(f"result: {r}")


if __name__ == "__main__":
    pass
    # change()
    # change_State()
