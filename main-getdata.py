


import json
from triplea.db.mongo_nav import change_reset_flag_llm_with_response, change_reset_flag_llm_with_template_id, get_article_info_with_llm_response,get_groupby_with_llm_response
from triplea.schemas.article import Article
# import triplea.service.llm as LLM_fx
from triplea.service.llm.calculate import precalculate
from triplea.service.llm.config_template import read_llm_template
import triplea.service.repository.persist as PERSIST
from triplea.config.settings import SETTINGS

if __name__ == "__main__":
          
    l_id = PERSIST.get_article_id_list_by_cstate(1, "FlagShortReviewByLLM")
    print(len(l_id))

    # id = l_id[1]
    # a = PERSIST.get_article_by_id(id)
    # updated_article = Article(**a.copy())
    # d = updated_article.ReviewLLM
    # print(type(d))
    # print(d[0]['Response'])
    # print(type(d[0]['Response']))
    # print(json.dumps(d[0]['Response'],sort_keys=True, indent=4))
    
    
    # ctn = d[0]['Response']['StringContent']
    # ctn = str.replace(ctn,'\n'," ")
    # print(ctn)
    n=0
    for i in l_id:
        a = PERSIST.get_article_by_id(i)
        article = Article(**a.copy())
        d = article.ReviewLLM
        # print(d[0]['OutputTokens'])
        if 'StringContent' in d[0]['Response']:
            n=n+1
            print(article.PMID)
            print("--------StringContent")
            print(d[0]['Response']['StringContent'])
            exit()

    print(f"Number of bad data : {n}")



    


