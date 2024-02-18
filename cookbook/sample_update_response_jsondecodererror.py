# Sample update response base of JSONDecodeError

import json
import time
from bson import ObjectId
from pymongo import MongoClient
import triplea.service.repository.persist as PERSIST
from triplea.schemas.article import Article, SourceBankType
from triplea.config.settings import SETTINGS
import triplea.service.llm as LLM_fx
from triplea.utils.general import print_error

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



import ast
if __name__ == "__main__":

    l_id = get_list_id()
    print(f"{len(l_id)} Records found.")
    for id in l_id:
        a = PERSIST.get_article_by_id(id)
        article = Article(**a.copy())
        for temp in article.ReviewLLM:
            json_error= True
            if temp['TemplateID'] == 'CardioBioBank1':
               if 'StringContent' in temp['Response']:
                    json_text =  temp['Response']['StringContent']
                    try:
                        new_response = json.loads(json_text)
                    except Exception as e:
                        if isinstance(e,json.JSONDecodeError):
                            if 'Expecting property name enclosed in double quotes' in e.msg:
                                try:
                                    if json_text[e.colno-2:e.colno-1] == ",":
                                        j = json_text[0:e.colno-2] + json_text[e.colno-1:len(json_text)]
                                        new_response = json.loads(json.dumps(j))
                                        json_error= False
                                    else:
                                        json_error= True
                                except Exception as error_double_quotes:
                                    pass
                                    json_error= True
                                    # print(type(error_double_quotes))
                                    # print(error_double_quotes)
                            elif 'Expecting value' in e.msg:
                                try:
                                    json_text = str.replace(json_text,'"', "'")
                                    new_response = json.loads(json.dumps(json_text))
                                    json_error= False
                                except Exception as error_expecting_value:
                                    json_error= True
                                    # print("----------------------Expecting value")
                                    # print(error_expecting_value.msg)
                                    # print(error_expecting_value.doc)
                                    # print(error_expecting_value.colno)
                                    # print(json_text[0:error_expecting_value.colno])
                            elif "Expecting ',' delimiter" in e.msg:
                                if json_text[e.colno-1:e.colno] == "+":
                                    json_error= True
                                    # "Sample": 9714 + 2203
                                elif json_text[e.colno-1:e.colno] == "/":
                                    json_error= True
                                    # "Sample" : 40114 // The given abstract mentions a sample size of 40114 adults. }
                                elif json_text[e.colno-1:e.colno] == "(":
                                    json_error= True
                                    # "Sample": 1513 (cases + controls)
                                elif json_text[e.colno-1:e.colno] == "_":
                                    json_error= True
                                    # "Sample" : 78707_GERD_cases_288734_controls
                                else:
                                    json_error= True
                                    # print(e.msg)
                                    # print(e.colno)
                                    # print(json_text[e.colno-1:e.colno])   
                                    # print(e.doc)
                            elif "Extra data" in e.msg:
                                # { "Include": false, "Biobanks": ["UK Biobank"], "Domain": [], "Sample": null }  T 
                                try:
                                    new_response = json.loads(json.dumps(json_text))
                                    json_error= False
                                except Exception as error_extra_data:
                                    json_error= True
                                    # print("----------------------Extra data")
                                    # print(error_expecting_value.msg)
                                    # print(error_expecting_value.doc)
                                    # print(error_expecting_value.colno)

                           
                            else:
                                json_error= True
                                # print("----------------------Else")
                                # print(e.msg)
                                # print(e.doc)
                                # print(e.colno)
                                # print(json_text[0:e.colno])

                            
                        else:
                            json_error= True
                            print("Error")
 


                    if json_error is False:
                        update_llm_response(id,'CardioBioBank1',new_response)
                        print(f"{id} update complete.")
                    else:
                        pass
                        # print(json_text)
                        # print("Error")


                






