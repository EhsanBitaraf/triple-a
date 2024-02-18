# This is sample programming for correct StringContent for convert json
# New method for replace F
# For T102

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




def get_f(new_text):
    fs = new_text.find('"F"')
    fe = new_text.find('"G"')
    f_value=new_text[fs+5:fe-2]
    return f_value

def replace_f(text,new_value):
    fs = text.find('"F"')
    fe = text.find('"G"')
    new_text = text[0:fs+5] + str(new_value) + text[fe-2:len(text)]
    return new_text
    

def last_soloution_cut_f(new_text):
    f= get_f(new_text)
    # I want cut f
    new_text=replace_f(new_text,-4)
    try:
        new_response = json.loads(new_text)
        print(type(new_response))
        new_response['CutF'] = f
        return new_response
    except:
        return False

def check_f(new_text):
        # Check F
        f= get_f(new_text)
        if isinstance(f,str):
            if len(f) < 9 :
                # like this 231,208
                f = str.replace(f,',','')
                try:
                    fint = int(f)
                except:
                    return False
                new_text=replace_f(new_text,fint)

                try:
                    new_response = json.loads(new_text)
                except:
                    return False
                return new_response
            elif len(f) > 10:
                plus = f.split("+")
                sum_plus=0
                for f1 in plus:
                    try:
                        f1= int(f1)
                    except Exception as exp:
                        
                        new_response = last_soloution_cut_f(new_text)
                        if new_response is False:
                            return False
                        else:
                            return new_response
                            
                    sum_plus = sum_plus + f1
                new_text=replace_f(new_text,sum_plus)
                try:
                    new_response = json.loads(new_text)
                except:
                    last_soloution_cut_f(new_text)
                    return False
                return new_response
        else:
            return False
            print("---------else--------")
            print(f)
            print(type(f))
            print("---------else--------")


def force_convert(new_text):
    try:
        new_response = json.loads(new_text)
    except Exception as e:
        # check_f(new_text)

        if "Expecting ',' delimiter" in e.msg:
            return False # Disable
            p1=new_text[0:e.colno-2]
            f_location=p1.find('"F"')
            if f_location == -1: # F Tag Not Exist
                return False
            else:
                deviation=len(p1)-f_location
                if deviation > 90:
                    print(e.doc)
                    print(p1)
                else:
                    return last_soloution_cut_f(new_text)
            return False

            
        elif 'Expecting property name enclosed in double quotes' in e.msg:
            
            print(e.doc)
            print(new_text[0:e.colno-2])
            return False


        elif 'Expecting value' in e.msg:
            return False

        else:
            # print(e.msg)
            # print(e.doc)
            # print("--------------------")
            # print(new_text[0:e.colno-2])
            return False                


if __name__ == "__main__":

    l_id = get_list_id()
    print(f"{len(l_id)} Records found.")
    n=0
    for id in l_id:
        a = PERSIST.get_article_by_id(id)
        article = Article(**a.copy())
        for temp in article.ReviewLLM:
            json_error= True
            if temp['TemplateID'] == 'T102':
               if 'StringContent' in temp['Response']:
                    n=n+1
                    new_text = temp['Response']['StringContent']
                    r = force_convert(new_text)
                    if r is False:
                       json_error= True
                    else:
                       json_error= False
                       new_response = r

            if json_error is False:
                update_llm_response(id,'T102',new_response)
                print(f"{id} update complete.") 
    print(n)                           
                   