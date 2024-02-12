import json
import os
import click
from triplea.config.settings import SETTINGS
from triplea.service.click_logger import logger
from triplea.schemas.article import Article
from triplea.service.repository.export.unified_export_json import json_converter_01
import triplea.service.repository.persist as persist
from triplea.utils.general import print_error, safe_csv


def export_triplea_json(proccess_bar=False, limit_sample=0) -> str:
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
                    f"There are {str(total_article_in_current_state - n)} article(s) left ... ",  # noqa: E501
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
            # ------------------Select ----------------------------------------
            output.append(updated_article)
            if proccess_bar:
                bar.label = "Article " + id + " exported. "
                bar.update(1)
            if limit_sample == 0:  # unlimited
                pass
            else:
                if n > limit_sample:
                    break
            # ------------------Select ----------------------------------------
        except Exception:
            print_error()

    final = json.dumps(output, default=lambda o: o.__dict__, indent=2)
    print()
    logger.INFO("Export Complete.")
    return final


def export_triplea_csv(proccess_bar=False, limit_sample=0) -> str:  # noqa: C901
    l_pmid = persist.get_all_article_pmid_list()
    logger.DEBUG(f"{str(len(l_pmid))} Article(s) Selected.")

    total_article_in_current_state = len(l_pmid)
    refresh_point = 0
    csv = ""
    csv = (
        csv
        + """key,title,authors,pmid,year,publisher,url,abstract,state,doi,keywords,topics"""  # noqa: E501
        + "\n"
    )
    n = 0
    for id in l_pmid:
        try:
            n = n + 1
            if refresh_point == 50:
                refresh_point = 0
                print()
                logger.INFO(
                    f"There are {str(total_article_in_current_state - n)} article(s) left ... ",  # noqa: E501
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
            # ------------------Select ----------------

            if updated_article.Title.__contains__(","):
                title = updated_article.Title.replace('"', " ")
                title = f'"{title}"'
            else:
                title = updated_article.Title

            authors = ""
            try:
                year = updated_article.OreginalArticle["PubmedArticleSet"][
                    "PubmedArticle"
                ]["MedlineCitation"]["Article"]["ArticleDate"]["Year"]
            except Exception:
                try:
                    year = updated_article.OreginalArticle["PubmedArticleSet"][
                        "PubmedArticle"
                    ]["MedlineCitation"]["Article"]["DateCompleted"]["Year"]
                except Exception:
                    try:
                        year = updated_article.OreginalArticle["PubmedArticleSet"][
                            "PubmedArticle"
                        ]["MedlineCitation"]["DateCompleted"]["Year"]
                    except Exception:
                        year = "0"

                        # with open("sample.json", "w") as outfile:
                        #     json.dump(updated_article.OreginalArticle, outfile)

            publisher = updated_article.Journal
            url = f"https://pubmed.ncbi.nlm.nih.gov/{updated_article.PMID}/"

            if updated_article.Abstract is None:
                abstract = ""
            else:
                if updated_article.Abstract.__contains__(","):
                    abstract = updated_article.Abstract.replace('"', " ")
                    abstract = f'"{abstract}"'
                else:
                    abstract = updated_article.Abstract

            doi = updated_article.DOI
            pmid = updated_article.PMID
            state = updated_article.State
            keywords = ""
            topics = ""

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

            csv = (
                csv
                + f"""{n},{title},{authors},{pmid},{year},{publisher},{url},{abstract},{state},{doi},{keywords},{topics}"""  # noqa: E501
                + "\n"
            )

            # ------------------Select ----------------
        except Exception:
            print_error()

    logger.INFO("Export Complete.")
    return csv


def export_triplea_csvs_in_relational_mode_save_file(  # noqa: C901
    output_file: str, proccess_bar=True, limit_sample=0
):  # noqa: C901
    l_id = persist.get_all_article_id_list()
    logger.DEBUG(f"{str(len(l_id))} Article(s) Selected.")

    total_article_in_current_state = len(l_id)

    if proccess_bar:
        bar = click.progressbar(length=len(l_id), show_pos=True, show_percent=True)

    refresh_point = 0
    csv = ""
    authors_csv = (
        "key,authors,affiliations,country,university,institute,center,hospital,department,location,email,zipcode"  # noqa: E501
        + "\n"
    )
    keywords_csv = "key,keywords" + "\n"
    topics_csv = "key,topics,rank" + "\n"
    csv = (
        csv
        + """key,title,pmid,year,publisher,url,abstract,state,doi,journal_issn,journal_iso_abbreviation,language,publication_type,citation"""  # noqa: E501
        + "\n"
    )
    n = 0
    # -------------------Create File-------------------------------
    file_name = os.path.basename(output_file)
    file = os.path.splitext(file_name)
    fname = file[0]
    fextention = file[1]

    dir = output_file.replace(fname + fextention, "")
    if fextention is None:
        fextention = ".csv"

    main_file = os.path.join(dir, fname + fextention)
    authors_file = os.path.join(dir, fname + "_authors" + fextention)
    keywords_file = os.path.join(dir, fname + "_keywords" + fextention)
    topics_file = os.path.join(dir, fname + "_topics" + fextention)

    with open(main_file, "w", encoding="utf-8") as file1:
        file1.write(csv)
        csv = ""

    with open(authors_file, "w", encoding="utf-8") as file2:
        file2.write(authors_csv)
        authors_csv = ""

    with open(keywords_file, "w", encoding="utf-8") as file3:
        file3.write(keywords_csv)
        keywords_csv = ""

    with open(topics_file, "w", encoding="utf-8") as file4:
        file4.write(topics_csv)
        topics_csv = ""

    f_main = open(main_file, "a", encoding="utf-8")
    f_authors = open(authors_file, "a", encoding="utf-8")
    f_keywords = open(keywords_file, "a", encoding="utf-8")
    f_topics = open(topics_file, "a", encoding="utf-8")

    for id in l_id:
        try:
            n = n + 1

            if refresh_point == SETTINGS.AAA_CLI_ALERT_POINT:
                refresh_point = 0
                if proccess_bar:
                    print()
                    logger.INFO(
                        f"There are {str(total_article_in_current_state - n)} article(s) left ",  # noqa: E501
                        forecolore="yellow",
                    )
                if proccess_bar is False:
                    bar.label = f"There are {str(total_article_in_current_state - n)} article(s) left "  # noqa: E501
                    bar.update(SETTINGS.AAA_CLI_ALERT_POINT)
            else:
                refresh_point = refresh_point + 1

            if limit_sample != 0:  # Unlimited
                if n > limit_sample:
                    break

            a = persist.get_article_by_id(id)
            # a = persist.get_article_by_pmid('18194356') # CRITICAL

            try:
                updated_article = Article(**a.copy())
            except Exception:
                raise Exception(f"Error in parsing article with ID = {id}")

            # -------------------------------------------------Parsing---------
            article = json_converter_01(updated_article)
            title = safe_csv(article["title"])
            year = article["year"]
            publisher = safe_csv(article["publisher"])
            journal_issn = article["journal_issn"]
            journal_iso_abbreviation = safe_csv(article["journal_iso_abbreviation"])
            language = safe_csv(article["language"])
            publication_type = safe_csv(article["publication_type"])
            url = article["url"]
            abstract = safe_csv(article["abstract"])
            doi = article["doi"]
            pmid = article["pmid"]
            state = article["state"]
            citation = article["citation_count"]

            if article["authors"] is not None:
                for au in updated_article.Authors:
                    if "affiliations" in au:
                        first_aff = au["affiliations"][0]
                        department = first_aff["department"]
                        hospital = first_aff["hospital"]
                        institute = first_aff["institute"]
                        country = first_aff["country"]
                        university = first_aff["university"]
                        center = first_aff["center"]
                        location = first_aff["location"]
                        email = first_aff["email"]
                        zipcode = first_aff["zipcode"]
                        aff = first_aff["text"]
                    else:
                        department = ""
                        hospital = ""
                        institute = ""
                        country = ""
                        university = ""
                        center = ""
                        location = ""
                        email = ""
                        zipcode = ""
                        aff = ""

                    str_aff = f"{safe_csv(country)},{safe_csv(university)},{safe_csv(institute)},{safe_csv(center)},{safe_csv(hospital)},{safe_csv(department)},{safe_csv(location)},{safe_csv(email)},{safe_csv(zipcode)}"  # noqa: E501
                    authors_csv = (
                        authors_csv
                        + f"{n},{safe_csv(au.FullName)},{safe_csv(aff)},{str_aff}"
                        + "\n"
                    )

            if "keywords" in article:
                if article["keywords"] is not None:
                    for k in article["keywords"]:
                        if k is not None:
                            keywords_csv = (
                                keywords_csv + f"{n},{safe_csv(k.Text)}" + "\n"
                            )  # noqa: E501

            if "topics" in article:
                if article["topics"] is not None:
                    for topic in article["topics"]:
                        if topic is not None:
                            topics_csv = (
                                topics_csv
                                + f"{n},{safe_csv(topic['text'])},{topic['rank']}"
                                + "\n"
                            )  # noqa: E501

            csv = (
                csv
                + f"""{n},{title},{pmid},{year},{publisher},{url},{abstract},{state},{doi},{journal_issn},{journal_iso_abbreviation},{language},{publication_type},{citation}"""  # noqa: E501
                + "\n"
            )

            if proccess_bar:
                bar.label = f"Article {id}, exported."
                bar.update(1)

            # ------------------Write to file ---------------------------------
            f_main.write(csv)
            csv = ""

            f_authors.write(authors_csv)
            authors_csv = ""

            f_keywords.write(keywords_csv)
            keywords_csv = ""

            f_topics.write(topics_csv)
            topics_csv = ""

        except Exception:
            print()
            print(f"id : {id}")
            print_error()

    f_main.close()
    f_authors.close()
    f_keywords.close()
    f_topics.close()
    print()
    logger.INFO("Export Complete.")
