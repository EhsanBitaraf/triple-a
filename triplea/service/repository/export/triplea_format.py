import json
import os
import sys

import click
from triplea.service.click_logger import logger
from triplea.schemas.article import Article
import triplea.service.repository.persist as persist
import traceback

from triplea.utils.general import safe_csv


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
    csv = csv + """key,title,authors,pmid,year,publisher,url,abstract,state,doi,keywords,topics""" + "\n"
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

            for topic in updated_article.Topics:
                topics = topics + topic + ";"
            
            if topics != "":
                if topics.__contains__(","):
                    topics = f'"{topics[:-1]}"'


            csv = csv + f"""{n},{title},{authors},{pmid},{year},{publisher},{url},{abstract},{state},{doi},{keywords},{topics}""" + "\n"


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

def export_triplea_csvs_in_relational_mode_save_file(output_file:str,
        proccess_bar=False,
        limit_sample=0):
    
    l_pmid = persist.get_all_article_pmid_list()
    logger.DEBUG(f"{str(len(l_pmid))} Article(s) Selected.")

    total_article_in_current_state = len(l_pmid)
    refresh_point = 0
    csv = ""
    authors_csv = "key,authors,affiliations" + "\n"
    keywords_csv = "key,keywords" + "\n"
    topics_csv="key,topics" + "\n"
    csv = csv + """key,title,pmid,year,publisher,url,abstract,state,doi,journal_issn,journal_iso_abbreviation,language,publication_type""" + "\n"
    n = 0
    for id in l_pmid:
        try:
            n = n + 1
            if refresh_point == 500:
                refresh_point = 0
                print()
                logger.INFO(
                    f"There are {str(total_article_in_current_state - n)} article(s) left ... ",
                    forecolore="yellow",
                )
            else:
                refresh_point = refresh_point + 1

            # a = persist.get_article_by_pmid(id)
            a = persist.get_article_by_pmid('21048984')
            
            try:
                updated_article = Article(**a.copy())
            except Exception:
                print()
                print(logger.ERROR(f"Error in parsing article. PMID = {id}"))
                raise Exception("Article Not Parsed.")




            title = ""
            year = ""
            publisher = ""
            journal_issn = ""
            journal_iso_abbreviation = ""
            language = ""
            publication_type = ""


            if updated_article.Title is not None:
                title = safe_csv(updated_article.Title)

            # try:
            #     year = updated_article.OreginalArticle['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['ArticleDate']['Year']
            # except:
            #     try:
            #         year = updated_article.OreginalArticle['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['DateCompleted']['Year'] 
            #     except:
            #         try:
            #             year = updated_article.OreginalArticle['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['DateCompleted']['Year'] 
            #         except: 
            #             year = "0"
            #             # with open("sample.json", "w") as outfile:
            #             #     json.dump(updated_article.OreginalArticle, outfile)
                

            try:
                year = updated_article.OreginalArticle['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate']['Year']
            except:
                try:
                    year = updated_article.OreginalArticle['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate']['MedlineDate']
                except:
                    year = "0"
                    # with open("sample.json", "w") as outfile:
                    #     json.dump(updated_article.OreginalArticle, outfile)            

            publisher = safe_csv(updated_article.Journal)
            try:
                journal_issn = updated_article.OreginalArticle['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['Journal']['ISSN']['#text']
            except:
                journal_issn = ""


            journal_iso_abbreviation = updated_article.OreginalArticle['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['Journal']['ISOAbbreviation']
            lang = updated_article.OreginalArticle['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['Language']
            if isinstance(lang,list):
                for l in lang:
                    language = l + ', ' + language
                language = language[:-1] 


            
            p = updated_article.OreginalArticle['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['PublicationTypeList']['PublicationType']
            if isinstance(p,list):
                for i in p:
                    chunk = i['#text']
                    publication_type = chunk + ', ' + publication_type
                # publication_type = p[0]['#text']
                publication_type = publication_type[:-1]
            else:
                publication_type = updated_article.OreginalArticle['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['PublicationTypeList']['PublicationType']['#text']
            
            journal_iso_abbreviation = safe_csv(journal_iso_abbreviation)
            language = safe_csv(language)
            publication_type = safe_csv(publication_type)

            

            url= f"https://pubmed.ncbi.nlm.nih.gov/{updated_article.PMID}/"

            if updated_article.Abstract is None:
                abstract = ""
            else:                
                if updated_article.Abstract.__contains__(","):
                    abstract = updated_article.Abstract.replace('"', ' ')
                    abstract = f'"{abstract}"' 
                else:
                    abstract = updated_article.Abstract
            doi = updated_article.DOI
            pmid = updated_article.PMID
            state = updated_article.State


            if updated_article.Authors is not None:
                for au in updated_article.Authors:
                    if au.Affiliations is not None:
                        aff = au.Affiliations[0].Text
                    else:
                        aff = None

                    authors_csv = authors_csv + f"{n},{safe_csv(au.FullName)},{safe_csv(aff)}" + "\n"

            if updated_article.Keywords is not None:
                for k in updated_article.Keywords:
                    if k is not None:
                        keywords_csv = keywords_csv + f"{n},{safe_csv(k.Text)}" + "\n"
                    
            if updated_article.Topics is not None:
                for topic in updated_article.Topics:
                    if topic is not None:
                        topics_csv = topics_csv + f"{n},{safe_csv(topic)}" + "\n"


            csv = csv + f"""{n},{title},{pmid},{year},{publisher},{url},{abstract},{state},{doi},{journal_issn},{journal_iso_abbreviation},{language},{publication_type}""" + "\n"


            #------------------Write to file ----------------
            file_name = os.path.basename(output_file)
            file = os.path.splitext(file_name)
            fname = file[0] 
            fextention = file[1]


            dir = output_file.replace(fname + fextention, '')
            if fextention is None:
                fextention= '.csv'

            main_file = os.path.join(dir, fname + fextention)
            authors_file = os.path.join(dir, fname + '_authors' + fextention)
            keywords_file = os.path.join(dir, fname + '_keywords' + fextention)
            topics_file = os.path.join(dir, fname + '_topics' + fextention)

            with open(main_file, "w", encoding="utf-8") as file1:
                file1.write(csv)

            with open(authors_file, "w", encoding="utf-8") as file2:
                file2.write(authors_csv)

            with open(keywords_file, "w", encoding="utf-8") as file3:
                file3.write(keywords_csv)

            with open(topics_file, "w", encoding="utf-8") as file4:
                file4.write(topics_csv)

        except Exception:
                exc_type, exc_value, exc_tb = sys.exc_info()
                print()
                print(f"line : {exc_tb.tb_lineno}")
                print(f"PMID : {updated_article.PMID}")
                logger.ERROR(f"Error {exc_type}")
                logger.ERROR(f"Error {exc_value}")
                traceback.print_tb(exc_tb)

    logger.INFO("Export Complete.")
