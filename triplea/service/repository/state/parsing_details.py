from triplea.schemas.article import Affiliation, Article, Author, Keyword
from triplea.service.click_logger import logger
import triplea.service.repository.persist as persist


def _convert_dict_to_class_affiliation(data: dict) -> Affiliation:
    """
    It takes a dictionary as input, and returns an Affiliation object

    :param data: dict
    :type data: dict
    :return: an Affiliation object
    """
    affiliation = Affiliation()
    affiliation.Text = data["Affiliation"]
    aff_part = affiliation.Text.split(",")
    aff_part_number = len(aff_part)
    affiliation.Part1 = aff_part[0]
    affiliation.Has_Extra = False
    if aff_part_number > 1:
        affiliation.Part2 = aff_part[1].strip()
    if aff_part_number > 2:
        affiliation.Part3 = aff_part[2].strip()
    if aff_part_number > 3:
        affiliation.Part4 = aff_part[3].strip()
    if aff_part_number > 4:
        affiliation.Part5 = aff_part[4].strip()
    if aff_part_number > 5:
        affiliation.Part6 = aff_part[5].strip()
    if aff_part_number > 6:
        affiliation.Has_Extra = True

    pre_hash = (
        str(affiliation.Part1)
        + str(affiliation.Part2)
        + str(affiliation.Part3)
        + str(affiliation.Part4)
    )
    affiliation.HashID = str(hash(pre_hash))
    return affiliation


def _convert_dict_to_class_author(data: dict) -> Author:
    """
    It takes a dictionary and returns an Author object

    :param data: dict
    :type data: dict
    :return: an Author object
    """
    if "CollectiveName" in data:
        my_author = Author()
        if "#text" in data["CollectiveName"]:
            my_author.FullName = data["CollectiveName"]["#text"]
        else:
            my_author.FullName = data["CollectiveName"]
        my_author.HashID = str(hash(my_author.FullName))
        return my_author

    my_author = Author()
    if "ForeName" in data:
        my_author.ForeName = data["ForeName"]
    my_author.LastName = data["LastName"]
    my_author.FullName = str(my_author.ForeName) + " " + my_author.LastName
    my_author.HashID = str(hash(my_author.FullName))
    if "Identifier" in data:
        if data["Identifier"]["@Source"] == "ORCID":
            my_author.ORCID = data["Identifier"]["#text"]

    if "AffiliationInfo" in data:
        affiliation_list = []
        if type(data["AffiliationInfo"]) == dict:
            affiliation = _convert_dict_to_class_affiliation(data["AffiliationInfo"])
            affiliation_list.append(affiliation)
        elif type(data["AffiliationInfo"]) == list:
            for aff in data["AffiliationInfo"]:
                affiliation = _convert_dict_to_class_affiliation(aff)
                affiliation_list.append(affiliation)
        else:
            raise NotImplementedError

        my_author.Affiliations = affiliation_list

    return my_author


def _convert_dict_to_class_keyword(data: dict) -> Keyword:
    """
    It takes a dictionary and returns a Keyword object

    :param data: the dictionary that contains the keyword information
    :type data: dict
    :return: A Keyword object
    """
    my_keyword = Keyword()
    if "#text" in data:
        my_keyword.Text = data["#text"]
    else:
        if "i" in data:
            my_keyword.Text = data["i"]  # in PMID 37283018
        else:  # in 34358588
            print()
            print("Warning in _convert_dict_to_class_keyword line 103.")
            my_keyword.Text = ""

    if "," in my_keyword.Text:
        pass
        # logger.ERROR ('The keyword text has the character ",".')
        # raise NotImplementedError
    if data["@MajorTopicYN"] == "Y":
        my_keyword.IS_Major = True
    else:
        my_keyword.IS_Major = False
    my_keyword.IS_Mesh = False
    return my_keyword


def _convert_dict_to_reffrence():
    pass


def parsing_details(article: Article) -> Article:
    article.State = 2
    backward_state = -1
    data = article.OreginalArticle

    if data is None:
        print()
        logger.ERROR(
            f"""Error in Original Article data. It is Null.
            PMID = {article.PMID}"""
        )
        article.State = backward_state
        return article

    # Read Original Article Format
    if "PubmedArticleSet" in data:
        if data["PubmedArticleSet"] is None:
            print()
            logger.ERROR(
                f"Error in Original Article data. It is Null. PMID = {article.PMID}"
            )
            article.State = backward_state
            return article

        if "PubmedArticle" in data["PubmedArticleSet"]:
            PubmedData = data["PubmedArticleSet"]["PubmedArticle"]["PubmedData"]
        else:
            print()
            article.State = backward_state
            logger.ERROR(
                f"Error in format Original Article data.  PMID = {article.PMID}"
            )
            return article
    else:
        print()
        logger.ERROR("Error in format Original Article data.")
        article.State = backward_state
        # data= json.dumps(data, indent=4)
        # with open("one-error-originalarticle.json", "w") as outfile:
        #     outfile.write(data)
        return article

    # The below code is checking if the article has a DOI or PMC number.
    # If it does, it will update the article with the DOI or PMC number.
    if "ArticleIdList" in PubmedData:
        ArticleId = PubmedData["ArticleIdList"]["ArticleId"]
        if type(ArticleId) == list:
            for a_id in ArticleId:
                if a_id["@IdType"] == "doi":
                    article.DOI = a_id["#text"]
                elif a_id["@IdType"] == "pmc":
                    article.PMC = a_id["#text"]
                else:
                    pass
                    # print()
                    # print(f'article() id type unhandel: {a_id["@IdType"]}')
        elif type(ArticleId) == dict:
            if ArticleId["@IdType"] == "doi":
                article.DOI = a_id["#text"]
            elif ArticleId["@IdType"] == "pmc":
                article.PMC = a_id["#text"]
            else:
                pass
                # print()
                # print(f'article id type unhandel: {a_id["@IdType"]}')

        else:
            raise NotImplementedError

    # Update Article Title & Journal Title.
    pubmed_article_data = data["PubmedArticleSet"]["PubmedArticle"]["MedlineCitation"][
        "Article"
    ]
    article.Title = pubmed_article_data["ArticleTitle"]
    if type(article.Title) == dict:
        article.Title = pubmed_article_data["ArticleTitle"]["#text"]
    article.Journal = pubmed_article_data["Journal"]["Title"]

    # The below code is checking if the abstract is a string or a list.
    # If it is a string, it will add the
    # abstract to the database. If it is a list,
    # it will add all the abstracts to the database.
    if "Abstract" in pubmed_article_data:
        if type(pubmed_article_data["Abstract"]) == dict:
            if type(pubmed_article_data["Abstract"]["AbstractText"]) == str:
                article.Abstract = pubmed_article_data["Abstract"]["AbstractText"]
            elif type(pubmed_article_data["Abstract"]["AbstractText"]) == list:
                abstract_all = ""
                for abstract_part in pubmed_article_data["Abstract"]["AbstractText"]:
                    abstract_all = abstract_all + " " + abstract_part["#text"]
                article.Abstract = abstract_all
            elif type(pubmed_article_data["Abstract"]["AbstractText"]) == dict:
                # exception happen in pmid '36497366' one-abstract-dict-mode.json
                article.Abstract = pubmed_article_data["Abstract"]["AbstractText"][
                    "#text"
                ]
            else:
                t = type(pubmed_article_data["Abstract"]["AbstractText"])
                logger.ERROR(f"Type {str(t)} in Abstract Not Implemented")
                raise NotImplementedError
        else:
            raise NotImplementedError

    # Creating a list of keywords. Merging Mesh List & Keyword List
    medline_citation = data["PubmedArticleSet"]["PubmedArticle"]["MedlineCitation"]
    keyword_list = []
    if "MeshHeadingList" in medline_citation:
        if type(medline_citation["MeshHeadingList"]["MeshHeading"]) == list:
            for mesh in medline_citation["MeshHeadingList"]["MeshHeading"]:
                my_keyword = Keyword()
                my_keyword.Text = mesh["DescriptorName"]["#text"]
                if mesh["DescriptorName"]["@MajorTopicYN"] == "Y":
                    my_keyword.IS_Major = True
                else:
                    my_keyword.IS_Major = False
                # mesh['QualifierName'] # We did not get into this subject
                my_keyword.IS_Mesh = True
                keyword_list.append(my_keyword)
        elif type(medline_citation["MeshHeadingList"]["MeshHeading"]) == dict:
            my_keyword = Keyword()
            mesh = medline_citation["MeshHeadingList"]["MeshHeading"]
            my_keyword.Text = mesh["DescriptorName"]["#text"]
            if mesh["DescriptorName"]["@MajorTopicYN"] == "Y":
                my_keyword.IS_Major = True
            else:
                my_keyword.IS_Major = False
            # mesh['QualifierName'] # We did not get into this subject
            my_keyword.IS_Mesh = True
            keyword_list.append(my_keyword)
        else:
            raise NotImplementedError

    if "KeywordList" in medline_citation:
        if type(medline_citation["KeywordList"]["Keyword"]) == list:
            for keyword in medline_citation["KeywordList"]["Keyword"]:
                my_keyword = _convert_dict_to_class_keyword(keyword)
                keyword_list.append(my_keyword)
        elif type(medline_citation["KeywordList"]["Keyword"]) == dict:
            my_keyword = _convert_dict_to_class_keyword(
                medline_citation["KeywordList"]["Keyword"]
            )
            keyword_list.append(my_keyword)
        else:
            raise NotImplementedError

    article.Keywords = keyword_list

    # The code is parsing the Article and
    # extracting the references from the Mode.
    if "ReferenceList" in PubmedData:
        if article.ReferenceCrawlerDeep is None:
            # raise Exception('ReferenceCrawlerDeep is None.')
            article.ReferenceCrawlerDeep = 0

        reference_list = []

        if isinstance(PubmedData["ReferenceList"], list):
            print(PubmedData["ReferenceList"])
            for ref in PubmedData["ReferenceList"]:
                if "ArticleIdList" in ref:
                    if type(ref["ArticleIdList"]["ArticleId"]) == dict:
                        if ref["ArticleIdList"]["ArticleId"]["@IdType"] == "pubmed":
                            reference_list.append(
                                ref["ArticleIdList"]["ArticleId"]["#text"]
                            )

                    elif type(ref["ArticleIdList"]["ArticleId"]) == list:
                        for ref_id in ref["ArticleIdList"]["ArticleId"]:
                            if ref_id["@IdType"] == "pubmed":
                                reference_list.append(ref_id["#text"])
                    else:
                        raise NotImplementedError

        else:
            if type(PubmedData["ReferenceList"]["Reference"]) == dict:
                ref = PubmedData["ReferenceList"]["Reference"]
                if "ArticleIdList" in ref:
                    if type(ref["ArticleIdList"]["ArticleId"]) == dict:
                        if ref["ArticleIdList"]["ArticleId"]["@IdType"] == "pubmed":
                            reference_list.append(
                                ref["ArticleIdList"]["ArticleId"]["#text"]
                            )

                    elif type(ref["ArticleIdList"]["ArticleId"]) == list:
                        for ref_id in ref["ArticleIdList"]["ArticleId"]:
                            if ref_id["@IdType"] == "pubmed":
                                reference_list.append(ref_id["#text"])
                    else:
                        raise NotImplementedError
            else:
                for ref in PubmedData["ReferenceList"]["Reference"]:
                    if "ArticleIdList" in ref:
                        if type(ref["ArticleIdList"]["ArticleId"]) == dict:
                            if ref["ArticleIdList"]["ArticleId"]["@IdType"] == "pubmed":
                                reference_list.append(
                                    ref["ArticleIdList"]["ArticleId"]["#text"]
                                )

                        elif type(ref["ArticleIdList"]["ArticleId"]) == list:
                            for ref_id in ref["ArticleIdList"]["ArticleId"]:
                                if ref_id["@IdType"] == "pubmed":
                                    reference_list.append(ref_id["#text"])
                        else:
                            raise NotImplementedError

        article.References = reference_list

        if article.ReferenceCrawlerDeep > 0:
            # Create new article from References List
            logger.DEBUG(
                f"Add {len(reference_list)} new article(s) by REFERENCE. ",
                forecolore="yellow",
                deep=3,
            )
            new_rcd = article.ReferenceCrawlerDeep - 1
            for ref_pmid in reference_list:
                persist.insert_new_pmid(pmid=ref_pmid, reference_crawler_deep=new_rcd)

    if "AuthorList" in pubmed_article_data:
        author_list = []
        if type(pubmed_article_data["AuthorList"]["Author"]) == list:
            for author in pubmed_article_data["AuthorList"]["Author"]:
                my_author = _convert_dict_to_class_author(author)
                author_list.append(my_author)
        elif type(pubmed_article_data["AuthorList"]["Author"]) == dict:
            my_author = _convert_dict_to_class_author(
                pubmed_article_data["AuthorList"]["Author"]
            )
            author_list.append(my_author)
        else:
            raise NotImplementedError
        article.Authors = author_list
    else:
        logger.WARNING(
            f"Article {article.PMID} has no AuthorList", forecolore="white", deep=5
        )

    return article
