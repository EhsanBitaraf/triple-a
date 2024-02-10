

from triplea.db.mongo_nav import get_article_title_and_abstract


def precalculate(time_taken_per_request:float,avarage_output_tokens:int):
    artilce_list = get_article_title_and_abstract()

    print(len(artilce_list))
    for a in artilce_list:
        print(a['Title'])
