from triplea.schemas.article import Affiliation, Article, Author, Keyword
from triplea.service.click_logger import logger
from triplea.utils.general import print_error


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
    )  # noqa: E501
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
        if isinstance(data["AffiliationInfo"], dict):
            affiliation = _convert_dict_to_class_affiliation(data["AffiliationInfo"])
            affiliation_list.append(affiliation)
        elif isinstance(data["AffiliationInfo"], list):
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


def parsing_details_pubmed(article: Article) -> Article:  # noqa: C901
    # current state may be 1
    article.State = 2  # next state
    backward_state = -1
    data = article.OreginalArticle
    try:
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
            if isinstance(ArticleId, list):
                for a_id in ArticleId:
                    if a_id["@IdType"] == "doi":
                        article.DOI = a_id["#text"]
                    elif a_id["@IdType"] == "pmc":
                        article.PMC = a_id["#text"]
                    else:
                        pass
                        # print()
                        # print(f'article() id type unhandel: {a_id["@IdType"]}')
            elif isinstance(ArticleId, dict):
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
        pubmed_article_data = data["PubmedArticleSet"]["PubmedArticle"][
            "MedlineCitation"
        ]["Article"]
        article.Title = pubmed_article_data["ArticleTitle"]
        if isinstance(article.Title, dict):
            article.Title = pubmed_article_data["ArticleTitle"]["#text"]
        article.Journal = pubmed_article_data["Journal"]["Title"]

        # The below code is checking if the abstract is a string or a list.
        # If it is a string, it will add the
        # abstract to the database. If it is a list,
        # it will add all the abstracts to the database.
        if "Abstract" in pubmed_article_data:
            if isinstance(pubmed_article_data["Abstract"], dict):
                if isinstance(pubmed_article_data["Abstract"]["AbstractText"], str):
                    article.Abstract = pubmed_article_data["Abstract"]["AbstractText"]
                elif isinstance(pubmed_article_data["Abstract"]["AbstractText"], list):
                    abstract_all = ""
                    structured_abstract = pubmed_article_data["Abstract"][
                        "AbstractText"
                    ]
                    for abstract_part in structured_abstract:
                        if "#text" in abstract_part:
                            abstract_all = (
                                abstract_all
                                + " "
                                + abstract_part["@Label"]
                                + ":"
                                + abstract_part["#text"]
                            )
                        else:  # observe in 37036022
                            abstract_all = (
                                abstract_all
                                + " "
                                + abstract_part["@Label"]
                                + ":"
                                + abstract_part["b"]
                            )

                    article.Abstract = abstract_all
                elif isinstance(pubmed_article_data["Abstract"]["AbstractText"], dict):
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
            if isinstance(medline_citation["MeshHeadingList"]["MeshHeading"], list):
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
            elif isinstance(medline_citation["MeshHeadingList"]["MeshHeading"], dict):
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
            if isinstance(medline_citation["KeywordList"]["Keyword"], list):
                for keyword in medline_citation["KeywordList"]["Keyword"]:
                    my_keyword = _convert_dict_to_class_keyword(keyword)
                    keyword_list.append(my_keyword)
            elif isinstance(medline_citation["KeywordList"]["Keyword"], dict):
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
                        if isinstance(ref["ArticleIdList"]["ArticleId"], dict):
                            if ref["ArticleIdList"]["ArticleId"]["@IdType"] == "pubmed":
                                reference_list.append(
                                    ref["ArticleIdList"]["ArticleId"]["#text"]
                                )

                        elif isinstance(ref["ArticleIdList"]["ArticleId"], list):
                            for ref_id in ref["ArticleIdList"]["ArticleId"]:
                                if ref_id["@IdType"] == "pubmed":
                                    reference_list.append(ref_id["#text"])
                        else:
                            raise NotImplementedError

            else:
                if isinstance(PubmedData["ReferenceList"]["Reference"], dict):
                    ref = PubmedData["ReferenceList"]["Reference"]
                    if "ArticleIdList" in ref:
                        if isinstance(ref["ArticleIdList"]["ArticleId"], dict):
                            if ref["ArticleIdList"]["ArticleId"]["@IdType"] == "pubmed":
                                reference_list.append(
                                    ref["ArticleIdList"]["ArticleId"]["#text"]
                                )

                        elif isinstance(ref["ArticleIdList"]["ArticleId"], list):
                            for ref_id in ref["ArticleIdList"]["ArticleId"]:
                                if ref_id["@IdType"] == "pubmed":
                                    reference_list.append(ref_id["#text"])
                        else:
                            raise NotImplementedError
                else:
                    for ref in PubmedData["ReferenceList"]["Reference"]:
                        if "ArticleIdList" in ref:
                            if isinstance(ref["ArticleIdList"]["ArticleId"], dict):
                                if (
                                    ref["ArticleIdList"]["ArticleId"]["@IdType"]
                                    == "pubmed"
                                ):
                                    reference_list.append(
                                        ref["ArticleIdList"]["ArticleId"]["#text"]
                                    )

                            elif isinstance(ref["ArticleIdList"]["ArticleId"], list):
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
                # new_rcd = article.ReferenceCrawlerDeep - 1
                for ref_pmid in reference_list:
                    pass
                    # CRITICAL Temporary disable for crawle REFERENCE
                    # persist.insert_new_pmid(pmid=ref_pmid,
                    #                          reference_crawler_deep=new_rcd)

        if "AuthorList" in pubmed_article_data:
            author_list = []
            if isinstance(pubmed_article_data["AuthorList"]["Author"], list):
                for author in pubmed_article_data["AuthorList"]["Author"]:
                    my_author = _convert_dict_to_class_author(author)
                    author_list.append(my_author)
            elif isinstance(pubmed_article_data["AuthorList"]["Author"], dict):
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


        article.links = f"https://pubmed.ncbi.nlm.nih.gov/{article.PMID}/"

        # ------------------------year--------------------------------
        try:
            article.Year = article.OreginalArticle["PubmedArticleSet"]["PubmedArticle"][
                "MedlineCitation"
            ]["Article"]["Journal"]["JournalIssue"]["PubDate"]["Year"]
        except Exception:
            try:
                article.Year = article.OreginalArticle["PubmedArticleSet"]["PubmedArticle"][
                    "MedlineCitation"
                ]["Article"]["Journal"]["JournalIssue"]["PubDate"]["MedlineDate"]
            except Exception:
                article.Year = "0"
                # with open("sample.json", "w") as outfile:
                #     json.dump(article.OreginalArticle, outfile)
        # ------------------------year--------------------------------

        # ------------------------ISSN--------------------------------
        try:
            article.SerialNumber = article.OreginalArticle["PubmedArticleSet"]["PubmedArticle"][
                "MedlineCitation"
            ]["Article"]["Journal"]["ISSN"]["#text"]
        except Exception:
            article.SerialNumber = ""
        # ------------------------ISSN--------------------------------

        # # ------------------------Journal ISO abv---------------------
        # journal_iso_abbreviation = article.OreginalArticle["PubmedArticleSet"][
        #     "PubmedArticle"
        # ]["MedlineCitation"]["Article"]["Journal"]["ISOAbbreviation"]
        # journal_iso_abbreviation = journal_iso_abbreviation
        # # ------------------------Journal ISO abv---------------------

        # ------------------------Language----------------------------
        lang = article.OreginalArticle["PubmedArticleSet"]["PubmedArticle"][
            "MedlineCitation"
        ]["Article"]["Language"]
        if isinstance(lang, list):
            for lg in lang:
                language = lg + ", " + language
            language = language[:-1]
        else:
            language = lang
        article.Language = language
        # ------------------------Language----------------------------

        # ------------------------Publication Type--------------------
        ptype_list = []
        p = article.OreginalArticle["PubmedArticleSet"]["PubmedArticle"]["MedlineCitation"][
            "Article"
        ]["PublicationTypeList"]["PublicationType"]
        if isinstance(p, list):
            for i in p:
                chunk = i["#text"]
                # publication_type = chunk + ", " + publication_type
                ptype_list.append(chunk)
            # publication_type = p[0]['#text']
            # publication_type = publication_type[:-1]
        else:
            publication_type = article.OreginalArticle["PubmedArticleSet"]["PubmedArticle"][
                "MedlineCitation"
            ]["Article"]["PublicationTypeList"]["PublicationType"]["#text"]
            ptype_list.append(publication_type)
        article.PublicationType = ptype_list
        # ------------------------Publication Type--------------------


        return article
    except Exception:
        article.State = backward_state
        print_error()
        return article
