


import json
from triplea.db.mongo_nav import change_reset_flag_llm_with_response, change_reset_flag_llm_with_template_id, get_article_info_with_llm_response,get_groupby_with_llm_response
from triplea.schemas.article import Article
# import triplea.service.llm as LLM_fx
from triplea.service.llm.calculate import precalculate
from triplea.service.llm.config_template import read_llm_template
import triplea.service.repository.persist as PERSIST
from triplea.config.settings import SETTINGS

if __name__ == "__main__":
    # precalculate(4.3,5)

    # read_llm_template()

  
    # output ="Yes"
    # data= get_article_info_with_llm_response(output)

    # with open(f'{output}.json', 'w', encoding='utf-8') as f:
    #     json.dump(data, f, ensure_ascii=False, indent=4)

    # id = "2109.02550v2" # Yes
    # a = PERSIST.get_article_by_arxiv_id(id)
    # r = LLM_fx.question_with_template_for_llm(a['Title'],a['Abstract'])
    # print(r)

    # #---------------------------------------------------------------
    # with open("gResp.json") as f:
    #     data = json.load(f)

    # for d in data:
    #     if d['Response'] == 'Unknown':
    #         print(f"Reset {d['_id']} ...")
    #         change_reset_flag_llm_with_response(d['_id'],'T101')
    # #-----------------------------------------------------
            
    l_id = PERSIST.get_article_id_list_by_cstate(1, "FlagShortReviewByLLM")

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
    for i in l_id:
        a = PERSIST.get_article_by_id(i)
        updated_article = Article(**a.copy())
        d = updated_article.ReviewLLM
        # print(d[0]['OutputTokens'])
        if 'StringContent' in d[0]['Response']:
            print(updated_article.PMID)
            print("--------StringContent")
            print(d[0]['Response']['StringContent'])



    


