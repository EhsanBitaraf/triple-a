import json
from tinydb import TinyDB, Query

class DataBase():
    pass

class DB_TinyDB(DataBase):
    db = TinyDB(DBROOTPATH / 'ehr.json')


if settings.SEPAS_EHR_DB_TYPE == 'Tiny':
    db = DB_TinyDB()
else:
    raise NotImplemented