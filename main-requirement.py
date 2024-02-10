

import json
import urllib

# from pypdf import PdfReader
from triplea.db.mongo_nav import change_reset_flag_llm_with_template_id, get_database_list
from triplea.schemas.article import Article
import triplea.service.llm as LLM_fx
from triplea.service.repository.export.triplea_format import export_triplea_csvs_in_relational_mode_save_file

from triplea.service.repository.state.initial_arxiv import get_article_list_from_arxiv_all_store_to_arepo
from triplea.service.repository.state.initial import get_article_list_from_pubmed_all_store_to_arepo
from triplea.service.repository.pipeline_core import move_state_forward
import triplea.service.repository.persist as PERSIST
import triplea.service.repository.pipeline_flag as cPIPELINE



if __name__ == "__main__":
    pass
    # # ------------------------Get List of Database-----------------------------
    # d= get_database_list()
    # print(d)
    # # ------------------------Get List of Database-----------------------------

    # # ------------------------Print RepoInfo-----------------------------------
    # PERSIST.print_article_info_from_repo()
    # # ------------------------Print RepoInfo-----------------------------------
    
    # # ------------------------Read Arxiv And Questuin From LLM-----------------
    # id = "1802.06018v2" 
    # a = PERSIST.get_article_by_arxiv_id(id)
    # r = LLM_fx.question_with_template_for_llm(a['Title'],a['Abstract'])
    # print(r)
    # # ------------------------Read Arxiv And Questuin From LLM-----------------

    # # ------------------------Read PMID And Questuin From LLM-----------------
    # id = "37301943"
    # id = "37301844" # No
    # id = "37301822" # No
    # id = "37301713" # Use BioBank Data
    # # id = "37300838"
    # # id = "5673991"
    # # id = "5782260"
    # # id = "5782261"
    # id = "37296187" # chert
    # id = "37285350"
    # id = "37282698"
    # id = "37278263" # chert
    # # id = "37268409" # description
    # id = "37301822"
    # a = PERSIST.get_article_by_pmid(id)
    # r = LLM_fx.question_with_template_for_llm(a['Title'],a['Abstract'])
    # print(r)

    # print(f"Response Type {type(r['Response'])}")
    
    # # d = json.loads(r['Response'])
    # # print(d)
    # # print(type(d))
    # # ------------------------Read PMID And Questuin From LLM-----------------

    # # ------------------------Run Short Review Article Pipeline----------------
    # cPIPELINE.go_article_review_by_llm()
    # # ------------------------Run Short Review Article Pipeline----------------

    # #---------------Reset FlagShortReviewByLLM to 0 ---------------------------
    # change_reset_flag_llm_with_template_id("T102")
    # #---------------Reset FlagShortReviewByLLM to 0 ---------------------------

    # Export
    # export_triplea_csvs_in_relational_mode_save_file("export.csv",limit_sample=120)




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


