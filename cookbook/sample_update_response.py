

import json
import time
from bson import ObjectId
from pymongo import MongoClient
import triplea.service.repository.persist as PERSIST
from triplea.schemas.article import Article, SourceBankType
from triplea.config.settings import SETTINGS
import triplea.service.llm as LLM_fx
from triplea.utils.general import print_error


# This is sample programming for correct StringContent for convert json

def get_list_id():
    _connection_url = SETTINGS.AAA_MONGODB_CONNECTION_URL
    client = MongoClient(_connection_url)
    db = client[SETTINGS.AAA_MONGODB_DB_NAME]   
    col_article = db["articledata"] 
    myquery = {"ReviewLLM.Response.StringContent": {"$exists": True}}
    cursor = col_article.find(
        myquery, projection={"SourceBank": "$SourceBank", "_id": 1}
    )
    # TODO _id

    la = list(cursor)
    new_la = []
    for c in la:
        new_la.append(c["_id"])

    if len(new_la) == 0:
        return []
    else:
        return new_la


def update_llm_response(document_id,template_id,new_response):
    _connection_url = SETTINGS.AAA_MONGODB_CONNECTION_URL
    client = MongoClient(_connection_url)
    db = client[SETTINGS.AAA_MONGODB_DB_NAME]
    col_article = db["articledata"]


    col_article.update_one(
        {"_id": ObjectId(document_id), "ReviewLLM.TemplateID": template_id},
        {"$set": {"ReviewLLM.$.Response": new_response}}
    )


def check_g_contains_double_quotation(new_text):
    gs = new_text.find('"G"')
    ge = new_text.find('}')
    g_value=new_text[gs+6:ge-1]
    if g_value.__contains__('"'):
        return True
    else:
        return False

def check_c_contains_double_quotation(new_text):
    cs = new_text.find('"C"')
    ce = new_text.find('", "D"')
    c_value=new_text[cs+6:ce]
    if c_value.__contains__('"'):
        return True
    else:
        return False
     
def replace_c_double_quotation(new_text):
    cs = new_text.find('"C"')
    ce = new_text.find('", "D"')
    c_value=new_text[cs+6:ce]
    while c_value.__contains__('"'):
        point = c_value.find('"')
        c_value = c_value[0:point] + "'" + c_value[point+1:len(c_value)]
    new_new_text = new_text[0:cs+6] + c_value + new_text[ce:len(new_text)]
    return new_new_text

def replace_g__double_quotation(new_text):
    gs = new_text.find('"G"')
    ge = new_text.find('}')
    g_value=new_text[gs+6:ge-1]
    while g_value.__contains__('"'):
        point = g_value.find('"')
        g_value = g_value[0:point] + "'" + g_value[point+1:len(g_value)]
    new_new_text = new_text[0:gs+6] + g_value + '"}'
    return new_new_text 



if __name__ == "__main__":

    l_id = get_list_id()
    print(f"{len(l_id)} Records found.")
    for id in l_id:
        a = PERSIST.get_article_by_id(id)
        article = Article(**a.copy())
        for temp in article.ReviewLLM:
            json_error= True
            if temp['TemplateID'] == 'T102':
               if 'StringContent' in temp['Response']:
                if isinstance(temp['Response']['StringContent'],str):
                    sc = temp['Response']['StringContent']
                    if sc[1:2] == "'":
                        new_text = str.replace(sc,"'",'"')
                        try:
                            new_response = json.loads(new_text)
                            # print(new_response)
                        except Exception:
                            json_error = True
                            if check_g_contains_double_quotation(new_text):
                                new_text = replace_g__double_quotation(new_text)
                                try:
                                    new_response = json.loads(new_text)
                                    json_error = False
                                except Exception:
                                    json_error = True
                                    if check_c_contains_double_quotation(new_text):
                                        new_text = replace_c_double_quotation(new_text)
                                        try:
                                            new_response = json.loads(new_text)
                                            json_error = False
                                        except Exception:
                                            json_error = True
                                            print(f"{id} json conversion error.")
                                            # print(new_text)

                        if json_error is False:
                            update_llm_response(id,'T102',new_response)
                            print(f"{id} update complete.")


                    elif sc[len(sc)-1:len(sc)] != "}":

                        new_text = sc + "}"
                        try:
                            new_response = json.loads(new_text)
                            json_error = False
                        except Exception:
                            json_error = True


                        if json_error is False:
                            update_llm_response(id,'T102',new_response)
                            print(f"{id} update complete.")                  
                    else:
                        fs = sc.find('"F"')
                        fe = sc.find('"G"')
                        f_value=sc[fs:fe]
                        print(f"-------> {f_value}")





