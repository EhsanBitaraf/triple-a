# Sample update response base of JSONDecodeError
# copy of sample_update_response_jsondecodererror
# for CardioBioBank1

import json
import time
from triplea.service.click_logger import logger
from bson import ObjectId
import click
from pymongo import MongoClient
import triplea.service.repository.persist as PERSIST
from triplea.schemas.article import Article, SourceBankType
from triplea.config.settings import SETTINGS
import triplea.service.llm as LLM_fx
from triplea.utils.general import print_error, print_pretty_dict

def get_list_id():
    _connection_url = SETTINGS.AAA_MONGODB_CONNECTION_URL
    client = MongoClient(_connection_url)
    db = client[SETTINGS.AAA_MONGODB_DB_NAME]   
    col_article = db["articledata"] 
    # myquery = {"ReviewLLM.Response.StringContent": {"$exists": True}}
    # myquery = {"ReviewLLM.TemplateID": "CardioBioBank1"}
    myquery = {"ReviewLLM.Response.StringContent": {"$exists": True},"ReviewLLM.TemplateID": "CardioBioBank1"}
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


def try_json_decoding(json_string):
    try:
        new_response = json.loads(json_string)
        return new_response
    except Exception as e:
        print()
        print(json_string)
        print(e.msg)
        return None

def error_analysis(response,json_error):
    if isinstance(json_error,json.JSONDecodeError):
        e = json_error
    else:
        print()
        print(f"Error type is not JSONDecodeError. It is {type(e)}.")
        return None
    

    if e.msg == 'Expecting property name enclosed in double quotes':
        print()
        logger.WARNING(f"Error: {e.msg}")
        print(response)
        logger.DEBUG(response[0:e.colno-2])
        logger.DEBUG("Please fix :")
        value = click.prompt("-->", type=str)
        response= response[0:e.colno-2] + value
        print(response)
        new_response = try_json_decoding(response)
        if new_response is None:
            return None
        else:
            logger.WARNING("Fixed")
            return new_response
    elif e.msg == 'Extra data':
        # "Sample" : "Over 300,000" }  Note: The sample size was not explicitly mentioned in the abstract,
        new_response = try_json_decoding(response[0:e.colno-1])
        if new_response is None:
            return None
        else:
            return new_response
    elif e.msg == "Expecting ',' delimiter":
        pass
        # "Sample" : 285 (acute COVID-19) + 77 (convalescent COVID-19) + 54 (controls) = 316
        # print()
        # print(response)
        # print(e.msg)
        return None
    else:
        print()
        print(response)
        print(e.msg)
        return None
        
def check_error_for_sample_cut_it(response,json_error):
    if isinstance(json_error,json.JSONDecodeError):
        e = json_error
    else:
        print()
        print(f"Error type is not JSONDecodeError. It is {type(e)}.")
        return None
    
    response[0:e.colno-1]
    start_tag = "Sample"
    tag_start = response.find(start_tag)
    if tag_start == -1:
        return None
    if e.colno > tag_start:
        tag_end=str.find(response,'}',tag_start)
        if len(response)-tag_end > 5:
            # print()
            # print("-----------------------------??------------")
            # print(response)
            # print("-----------------------------??------------")
            return None
        else:
            # print()
            # print(response)
            # print()      
            sample_value = response[tag_start+len(start_tag)+3:tag_end]
            new_response=response[0:tag_start+len(start_tag)+3] + str(-3) + "}"
            new_response = try_json_decoding(new_response)
            if new_response is None:
                return None
            else:
                new_response['Sample1'] = sample_value
                # print_pretty_dict(new_response)
                return new_response
    else:
        return None


def fx_response_remodel(response):
    if isinstance(response,dict):
        if 'StringContent' in response:
            response = response['StringContent']
            response = str.replace(response,"'",'"')
            response = str.replace(response,"False","false")
            response = str.replace(response,"True","true")
            try:
                new_response = json.loads(response)
                return new_response
            except Exception as e:
                if isinstance(e,json.JSONDecodeError):
                    # For Analysis Error and Try one more time
                    # new_try_response = error_analysis(response,e)
                    new_try_response = check_error_for_sample_cut_it(response,e)
                    if new_try_response is None:
                        return None
                    else:
                        return new_try_response
                    
                    # If you don't want try again
                    new_response = {"StringContent": response,
                                    "ErrorMsg" : e.msg }                   
                    # return new_response # if you want update error message
                    return None # if you not want update error message
                else:
                    new_response = {"StringContent": response,
                                    "ErrorMsg" : type(e) }
                    return new_response # if you want update error message
                    return None # if you not want update error message
        else:
            return None
    else:
        return None

def remodel_llm_response(remodel_fx,
                         template_id:str,
                         limit_sample = 0,
                         proccess_bar = True):
    l_id = get_list_id()
    logger.DEBUG(f"{len(l_id)} Records found.")
    doc_number = len(l_id)
    if doc_number == 0:
        return
    n = 0
    updated_number = 0
    if proccess_bar:
        bar = click.progressbar(length=doc_number, show_pos=True, show_percent=True)
        bar.label = f"{len(l_id)} Records found..."
        bar.update(1)

    for id in l_id:
        n = n + 1
        try:
            a = PERSIST.get_article_by_id(id)
            article = Article(**a.copy())
            need_update = False
            new_response = None
            for temp in article.ReviewLLM:
                if temp['TemplateID'] == template_id:
                    if 'Response' in temp:
                        new_response = remodel_fx(temp['Response'])
                        if new_response is None:
                            need_update = False
                        else:
                            need_update = True
                    else:
                        need_update = False


            # if needed uodate
            if need_update is True:
                if isinstance(new_response,dict):
                    update_llm_response(id,template_id,new_response)
        
                    # For View Proccess
                    updated_number = updated_number + 1
                    if proccess_bar:
                        bar.label = f"""{id} update complete. {updated_number} Article(s) Updated."""
                        bar.update(n_steps = 1,current_item=n)
                else:
                    raise Exception("Response is not Dict!")
            else:
                if proccess_bar:
                    bar.update(1)


            if limit_sample != 0:  # Unlimited
                if n > limit_sample:
                    break
        except Exception:
            print()
            print(logger.ERROR(f"article. ID = {id}"))
            print_error()    

if __name__ == "__main__":
    remodel_llm_response(fx_response_remodel,"CardioBioBank1",limit_sample = 0,proccess_bar = True)