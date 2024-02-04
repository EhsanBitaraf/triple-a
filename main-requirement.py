

import urllib

from pypdf import PdfReader
from triplea.db.mongo_nav import get_database_list

from triplea.service.repository.state.initial_arxiv import get_article_list_from_arxiv_all_store_to_arepo
from triplea.service.repository.state.initial import get_article_list_from_pubmed_all_store_to_arepo
from triplea.service.repository.pipeline_core import move_state_forward
import triplea.service.repository.persist as PERSIST

def page_cleaner(page):
    p1 = page.extract_text()
    p1 = p1.replace('-\n'," ")
    sen = p1.split('\n')
    
    for line in range(len(sen)):
        
        if line>10 and len(sen[line]) > 1:
            # this for title end author name
            len_line = len(sen[line])

            lastch =  sen[line][-1]
            if line +1 != len(sen):
                try:
                    if len_line> 15 and len(sen[line+1])> 15 and lastch !=".":
                        new = sen[line].replace('\n', " ") + sen[line+1]
                        sen[line] = new
                        sen[line+1] = ""
                except Exception:
                    print (line)
                    print(len(sen))
                    raise


    text_file=""
    for s in sen:
        if s != "":
            text_file= text_file  + s + '\n'
            # print(s)
    
    return text_file




if __name__ == "__main__":


    # d= get_database_list()
    # print(d)
    
    # # Step 1 - Get article from Arxiv
    # arxiv_search_string = 'ti:"large language model" AND ti:Benchmark AND abs:medical'
    # get_article_list_from_arxiv_all_store_to_arepo(arxiv_search_string,0,10)

    # # Step 2 - Get article from Pubmed
    # pubmed_search_string = '("large language model"[Title]) AND (Benchmark[Title/Abstract])'
    # get_article_list_from_pubmed_all_store_to_arepo(pubmed_search_string)
 


    # Step 3 - Get info
    PERSIST.print_article_info_from_repo()

    # # Step 4 - Moving from `0` to `1`
    # move_state_forward(0)                    

    # # Step 5 - Moving from `1` to `2`
    # move_state_forward(1)
                    
    # # Step 6 - Moving from `2` to `3`
    # move_state_forward(2)

    # # Step 7 - Moving from `3` to `4`
    # move_state_forward(3)

    # Step 8 - Moving from `4` to `5`
    move_state_forward(4)

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


