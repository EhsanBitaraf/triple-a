

import json
import urllib

from bson import ObjectId
from triplea.config.settings import SETTINGS

# from pypdf import PdfReader
from triplea.db.mongo_nav import change_reset_flag_affiliation_mining, change_reset_flag_llm_with_template_id, get_database_list
from triplea.schemas.article import Article
import triplea.service.llm as LLM_fx
from triplea.service.llm.calculate import post_calculate, precalculate
from triplea.service.llm.recycle import reset_flag_llm_by_function
from triplea.service.repository.export.triplea_format import export_triplea_csvs_in_relational_mode_save_file
from triplea.service.repository.import_file.ris_parser import import_ris_file

from triplea.service.repository.state.custom import affiliation_mining_titipata_integration
from triplea.service.repository.state.initial_arxiv import get_article_list_from_arxiv_all_store_to_arepo
from triplea.service.repository.state.initial import get_article_list_from_pubmed_all_store_to_arepo
from triplea.service.repository.pipeline_core import move_state_forward
import triplea.service.repository.persist as PERSIST
import triplea.service.repository.pipeline_flag as cPIPELINE
from triplea.utils.general import print_pretty_dict



if __name__ == "__main__":
    pass
    print(SETTINGS.VERSION)


    # # ------------------------test-----------------
    # id = "65d46589604437efd5da91cd"
    # id = ObjectId(id)
    # a = PERSIST.get_article_by_id(id)
    # article = Article(**a.copy())
    # ua = affiliation_mining_titipata_integration.affiliation_mining_titipata_integration(article)
    
    # # print_pretty_dict(ua)
    # # ------------------------test-----------------

    # # ------------------------Get List of Database-----------------------------
    # d= get_database_list()
    # print(d)
    # # ------------------------Get List of Database-----------------------------

    # # ------------------------Print RepoInfo-----------------------------------
    # PERSIST.print_article_info_from_repo()
    # # ------------------------Print RepoInfo-----------------------------------

    
    # # ------------------------Read Arxiv And Questuin From LLM-----------------
    # id = "2312.12806v1" 
    # a = PERSIST.get_article_by_arxiv_id(id)
    # prompt = LLM_fx.get_prompt_with_template(a['Title'],a['Abstract'])
    # print(prompt)
    # r = LLM_fx.question_with_template_for_llm(a['Title'],a['Abstract'])
    # print_pretty_dict(r)
    # # ------------------------Read Arxiv And Questuin From LLM-----------------

    # # ------------------------Read PMID And Question From LLM-----------------
    # id = "33675346"
    # a = PERSIST.get_article_by_pmid(id)
    # prompt = LLM_fx.get_prompt_with_template(a['Title'],a['Abstract'])
    # print(prompt)
    # r = LLM_fx.question_with_template_for_llm(a['Title'],a['Abstract'])
    # print(r)
    # # ------------------------Read PMID And Question From LLM-----------------

    # # ------------------------Read id And Question From LLM-----------------
    # id = "65ffbf945fbe2581ad699b80"
    # id = ObjectId("65ffbf945fbe2581ad699b80")
    # a = PERSIST.get_article_by_id(id)
    # prompt = LLM_fx.get_prompt_with_template(a['Title'],a['Abstract'])
    # print(prompt)
    # r = LLM_fx.question_with_template_for_llm(a['Title'],a['Abstract'])
    # print(r)

    # print(f"Response Type {type(r['Response'])}")
    
    # # ------------------------Read PMID And Question From LLM-----------------



    # # ------------------------Run Short Review Article Pipeline----------------
    # cPIPELINE.go_article_review_by_llm()
    # # ------------------------Run Short Review Article Pipeline----------------


    # #---------------Reset FlagShortReviewByLLM to 0 ---------------------------
    # change_reset_flag_llm_with_template_id("T102")
    # #---------------Reset FlagShortReviewByLLM to 0 ---------------------------

    # #----------------------Get Result or Specific LLM Response-----------------
    # output ="Yes"
    # data= get_article_info_with_llm_response(output)

    # with open(f'{output}.json', 'w', encoding='utf-8') as f:
    #     json.dump(data, f, ensure_ascii=False, indent=4)
    # #----------------------Get Result or Specific LLM Response-----------------

    # #-------------------------Reset LLM Respose With Specific Response--------
    # with open("gResp.json") as f:
    #     data = json.load(f)

    # for d in data:
    #     if d['Response'] == 'Unknown':
    #         print(f"Reset {d['_id']} ...")
    #         change_reset_flag_llm_with_response(d['_id'],'T101')
    # #-------------------------Reset LLM Respose With Specific Response--------

    # #-------------------------Reset FlagShortReviewByLLM to 0 with fx----------

    # def my_fx(TemplateID, lr):
    #     # True Must Be Updated
    #     for r in lr:
    #         if 'Response' in r:
    #             if r['Response'] == 'Yes,':
    #                 return True
    #             elif r['Response'] == 'Yes':
    #                 return True
    #             elif r['Response'] == 'No' or r['Response'] == '"No' or r['Response'] == 'No,' or r['Response'] == 'No.':
    #                 return False
    #             elif r['Response'][:3] == 'No,':
    #                 return False
    #             elif r['Response'][:4] == 'Yes,':
    #                 return True

    #             else:
                    
    #                 # print(r['Response'])
    #                 return True                    
    #         else:
    #             print(r)
    #             return False


    # reset_flag_llm_by_function("T101",my_fx,limit_sample=0)
    # print()
    # #-------------------------Reset FlagShortReviewByLLM to 0 with fx----------

    # -------------------------------Export csvs-------------------------------
    # export_triplea_csvs_in_relational_mode_save_file("export.csv",limit_sample=120)
    # -------------------------------Export csvs-------------------------------



    # reader = PdfReader("2310.15773v1.pdf")
    # page1 = reader.pages[0]
    # page2 = reader.pages[1]

    # # meta = reader.metadata
    # # print(meta.author)
    # # print(meta.creator)
    # # print(meta.producer)
    # # print(meta.subject)
    # # print(meta.title)
    # for i in page2.get_object():
    #     print(i)
    #     # print(i.get_object())
    #     print(i.extract_text())
    # # for page in page1:
    # #     if "/Annots" in page:
    # #         for annot in page["/Annots"]:
    # #             obj = annot.get_object()
    # #             annotation = {"subtype": obj["/Subtype"], "location": obj["/Rect"]}
    # #             print(annotation)

    # # print(page2.get_object())
    # text_file = page_cleaner(reader.pages[0])
    # text_file = text_file + '\n' + page_cleaner(reader.pages[1])
    # f = open("ArxivID3.txt", "w")
    # f.write(text_file)
    # f.close()

    # from unstructured.partition.auto import partition
    # filename = "2310.15773v1.pdf"
    # with open(filename, "rb") as f:
    #     elements = partition(file=f, include_page_breaks=True)

    # print(elements[1].to_dict())
    # # for i  in elements:
    # #     print(i)
    # # print("\n\n".join([str(el) for el in elements][5:15]))


