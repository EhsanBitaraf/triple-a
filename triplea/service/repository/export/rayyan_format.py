import sys
from triplea.service.click_logger import logger
from triplea.schemas.article import Article
import triplea.service.repository.persist as persist
import traceback


"""
This function exports article data from a database to a CSV file in a specific format.

Inputs:
- None

Outputs:
- A string containing the CSV data representing the exported articles.

Example Usage:
csv_data = export_rayyan_csv()
print(csv_data)

Code Analysis:
1. Retrieve a list of PubMed IDs (PMIDs) from the database.
2. Initialize variables for tracking the total number of articles and the number of articles processed.
3. Initialize variables for storing the CSV data, nodes, and edges.
4. Iterate over each PMID in the list.
5. Retrieve the article data from the database using the PMID.
6. Parse the article data and extract the relevant fields.
7. Format the fields and append them to the CSV data.
8. Return the CSV data.
"""


def export_rayyan_csv() -> str:
    l_pmid = persist.get_all_article_pmid_list()
    logger.DEBUG(f"{str(len(l_pmid))} Article(s) Selected.")

    total_article_in_current_state = len(l_pmid)
    number_of_article_move_forward = 0

    refresh_point = 0
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
            if refresh_point == 50:
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
                try:
                    year = updated_article.OreginalArticle["PubmedArticleSet"][
                        "PubmedArticle"
                    ]["MedlineCitation"]["Article"]["DateCompleted"]["Year"]
                except:
                    try:
                        year = updated_article.OreginalArticle["PubmedArticleSet"][
                            "PubmedArticle"
                        ]["MedlineCitation"]["DateCompleted"]["Year"]
                    except:
                        year = "0"

                        # with open("sample.json", "w") as outfile:
                        #     json.dump(updated_article.OreginalArticle, outfile)

            publisher = ""
            url = f"https://pubmed.ncbi.nlm.nih.gov/{updated_article.PMID}/"

            if updated_article.Abstract is None:
                abstract = ""
            else:
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

    # print(os.path.join('/path/to/Documents',"completeName"))

    # with open("rayyan.csv", "w", encoding="utf-8") as file1:
    #     file1.write(csv)
    logger.INFO("Export Complete.")
    return csv
