

from pymongo import MongoClient
from triplea.config.settings import SETTINGS

connection_url = SETTINGS.AAA_MONGODB_CONNECTION_URL
print(connection_url)
client = MongoClient(connection_url)
# db = client[SETTINGS.AAA_MONGODB_DB_NAME]
# col_article = db["articledata"]

def get_database_list():
    dbs = client.database_names()
    return dbs


