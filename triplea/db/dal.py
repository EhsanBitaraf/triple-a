from triplea.config.settings import SETTINGS
from triplea.db.mongodb import DB_MongoDB
from triplea.db.tinydb import DB_TinyDB


if SETTINGS.AAA_DB_TYPE == "TinyDB":
    db = DB_TinyDB()
elif SETTINGS.AAA_DB_TYPE == "MongoDB":
    db = DB_MongoDB()
else:
    raise NotImplementedError


if __name__ == "__main__":
    ddb = DB_TinyDB()
    # a = ddb.is_article_exist_by_pmid('3670594')

    # ddb.db.drop_table('node')
    # ddb.db.drop_table('edge')
