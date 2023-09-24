import json
import sys

import click
from triplea.service.click_logger import logger
from triplea.schemas.article import Article
import triplea.service.repository.persist as persist
import traceback



def export_triplea_json(proccess_bar=False, limit_sample=0)-> str:
    l_pmid = persist.get_all_article_pmid_list()
    logger.DEBUG(f"{str(len(l_pmid))} Article(s) Selected.")

    total_article_in_current_state = len(l_pmid)
    n = 0

    if proccess_bar:
        bar = click.progressbar(length=len(l_pmid), show_pos=True, show_percent=True)

    refresh_point = 0

    output = []
    for id in l_pmid:
        try:
            n = n + 1
            if refresh_point == 50:
                refresh_point = 0
                print()
                logger.INFO(
                    f"There are {str(total_article_in_current_state - n)} article(s) left ... ",
                    forecolore="yellow",
                )
            else:
                refresh_point = refresh_point + 1

            a = persist.get_article_by_pmid(id)
            try:
                updated_article = Article(**a.copy())
            except Exception:
                print()
                print(logger.ERROR(f"Error in parsing article. PMID = {id}"))
                raise Exception("Article Not Parsed.")
            #------------------Select ----------------
            output.append (updated_article)
            if proccess_bar:
                bar.label = (
                    "Article "
                    + id
                    + " exported. "
                )
                bar.update(1)            
            if limit_sample == 0: # unlimited
                pass
            else:
                if n > limit_sample:
                    break
            #------------------Select ----------------
        except Exception:
                exc_type, exc_value, exc_tb = sys.exc_info()
                print()
                print(exc_tb.tb_lineno)
                logger.ERROR(f"Error {exc_type}")
                logger.ERROR(f"Error {exc_value}")
                traceback.print_tb(exc_tb)

    final = json.dumps(output, default=lambda o: o.__dict__, indent=2)
    print()
    logger.INFO("Export Complete.")
    return final

def export_triplea_csv(proccess_bar=False, limit_sample=0)-> str:
    l_pmid = persist.get_all_article_pmid_list()
    logger.DEBUG(f"{str(len(l_pmid))} Article(s) Selected.")

    total_article_in_current_state = len(l_pmid)
    refresh_point = 0
    csv = ""
    csv = csv + """key,title,authors,pmid,year,publisher,url,abstract,state,doi,keywords""" + "\n"
    n = 0
    for id in l_pmid:
        try:
            n = n + 1
            if refresh_point == 50:
                refresh_point = 0
                print()
                logger.INFO(
                    f"There are {str(total_article_in_current_state - n)} article(s) left ... ",
                    forecolore="yellow",
                )
            else:
                refresh_point = refresh_point + 1

            a = persist.get_article_by_pmid(id)
            try:
                updated_article = Article(**a.copy())
            except Exception:
                print()
                print(logger.ERROR(f"Error in parsing article. PMID = {id}"))
                raise Exception("Article Not Parsed.")
            #------------------Select ----------------


            if updated_article.Title.__contains__(","):
                title = updated_article.Title.replace('"', ' ')
                title = f'"{title}"' 
            else:
                title = updated_article.Title
                
            authors = ""
            try:
                year = updated_article.OreginalArticle['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['ArticleDate']['Year']
            except:
                try:
                    year = updated_article.OreginalArticle['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['DateCompleted']['Year'] 
                except:
                    try:
                        year = updated_article.OreginalArticle['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['DateCompleted']['Year'] 
                    except: 
                        year = "0"
                    

                        # with open("sample.json", "w") as outfile:
                        #     json.dump(updated_article.OreginalArticle, outfile)
                

            publisher = updated_article.Journal
            url= f"https://pubmed.ncbi.nlm.nih.gov/{updated_article.PMID}/"

            if updated_article.Abstract is None:
                abstract = ""
            else:                
                if updated_article.Abstract.__contains__(","):
                    abstract = updated_article.Abstract.replace('"', ' ')
                    abstract = f'"{abstract}"' 
                else:
                    abstract = updated_article.Abstract
            notes = ""
            doi = updated_article.DOI
            pmid = updated_article.PMID
            state = updated_article.State
            keywords = ""


            for au in updated_article.Authors:
                authors = authors + au.FullName + ","

            if authors != "":
                authors = f'"{authors[:-1]}"'

            for k in updated_article.Keywords:
                keywords = keywords + k.Text + ";"
            
            if keywords != "":
                if keywords.__contains__(","):
                    keywords = f'"{keywords[:-1]}"'


            csv = csv + f"""{n},{title},{authors},{pmid},{year},{publisher},{url},{abstract},{state},{doi},{keywords}""" + "\n"


            #------------------Select ----------------
        except Exception:
                exc_type, exc_value, exc_tb = sys.exc_info()
                print()
                print(exc_tb.tb_lineno)
                logger.ERROR(f"Error {exc_type}")
                logger.ERROR(f"Error {exc_value}")
                traceback.print_tb(exc_tb)

    logger.INFO("Export Complete.")
    return csv

