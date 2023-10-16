# flake8: noqa
# noqa: F401

import click
import time
import sys
import json
import re
import networkx as nx
from pymongo import MongoClient
from triplea.config.settings import SETTINGS
from triplea.service.click_logger import logger
from triplea.schemas.article import Article
from triplea.schemas.node import Node
from triplea.service.graph.analysis.info import info
import triplea.service.repository.persist as persist
import triplea.service.graph.export.export as gexport
import triplea.service.graph.analysis.ganalysis as ganaliz
import traceback
import os


# # Export Selected Article For Rayyan

if __name__ == "__main__":
    connection_url = SETTINGS.AAA_MONGODB_CONNECTION_URL
    client = MongoClient(connection_url)
    db = client[SETTINGS.AAA_MONGODB_DB_NAME]
    db = client["articledata"]
    col_article = db["articledata"]

    myquery = {
        "$or": [
            {"Topics": re.compile(".*biobank.*", re.IGNORECASE)},
            {"Topics": re.compile(".*biobank.*", re.IGNORECASE)},
            {"Topics": re.compile(".*bio-bank.*", re.IGNORECASE)},
        ]
    }
    cursor = col_article.find(myquery, projection={"PMID": "$PMID", "_id": 0})
    l_pmid = []
    for a in list(cursor):
        l_pmid.append(a["PMID"])
    logger.DEBUG(f"{str(len(l_pmid))} Article(s) Selected.")

    total_article_in_current_state = len(l_pmid)
    number_of_article_move_forward = 0

    refresh_point = 0
    nodes = []
    edges = []
    csv = ""
    csv = (
        csv
        + """key,title,authors,issn,volume,issue,pages,year,publisher,url,abstract,notes,doi,keywords"""
        + "\n"
    )
    n = 0
    for id in l_pmid:
        try:
            number_of_article_move_forward = number_of_article_move_forward + 1
            if refresh_point == 500:
                refresh_point = 0
                print()
                logger.INFO(
                    f"There are {str(total_article_in_current_state - number_of_article_move_forward)} article(s) left ... ",
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
            if updated_article.Title.__contains__(
                "biobank"
            ) or updated_article.Title.__contains__("Biobank"):
                n = n + 1
                if updated_article.Title.__contains__(","):
                    title = updated_article.Title.replace('"', " ")
                    title = f'"{title}"'
                else:
                    title = updated_article.Title

                authors = ""
                issn = ""
                volume = ""
                issue = ""
                pages = ""
                try:
                    year = updated_article.OreginalArticle["PubmedArticleSet"][
                        "PubmedArticle"
                    ]["MedlineCitation"]["Article"]["ArticleDate"]["Year"]
                except:
                    year = ""
                publisher = ""
                url = f"https://pubmed.ncbi.nlm.nih.gov/{updated_article.PMID}/"
                if updated_article.Abstract.__contains__(","):
                    abstract = updated_article.Abstract.replace('"', " ")
                    abstract = f'"{abstract}"'
                else:
                    abstract = updated_article.Abstract
                notes = ""
                doi = ""
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

                csv = (
                    csv
                    + f"""{n},{title},{authors},{issn},{volume},{issue},{pages},{year},{publisher},{url},{abstract},{notes},{doi},{keywords}"""
                    + "\n"
                )

            # ------------------Select ----------------
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            print()
            print(exc_tb.tb_lineno)
            logger.ERROR(f"Error {exc_type}")
            logger.ERROR(f"Error {exc_value}")
            traceback.print_tb(exc_tb)

    print(os.path.join("/path/to/Documents", "completeName"))

    with open("rayyan.csv", "w", encoding="utf-8") as file1:
        file1.write(csv)
    logger.INFO("Export Complete.")
