from triplea.schemas.article import Article, Author, SourceBankType
import warnings

def _json_converter_author_general(author: Author):
    warnings.warn(
        """_json_converter_author_general() is deprecated
 and will be removed in a future version.
 New function is _converter_authors_to_short""",
        DeprecationWarning,
        stacklevel=2
    )
    fullname = ""

    fullname = author.FullName

    affiliation_list = []
    if author.Affiliations is not None:
        for one_aff in author.Affiliations:
            # first_aff = author.Affiliations[0]
            department = ""
            hospital = ""
            institute = ""
            country = ""
            university = ""
            center = ""
            location = ""
            email = ""
            zipcode = ""

            if one_aff.Structural is not None:
                for s in one_aff.Structural:
                    if "department" in s:
                        department = s["department"]
                    elif "hospital" in s:
                        hospital = s["hospital"]
                    elif "institute" in s:
                        institute = s["institute"]
                    elif (
                        "institution" in s
                    ):  # aff.ParseMethod = AffiliationParseMethod.TITIPATA_API  # noqa: E501
                        institute = s["institution"]
                    elif "country" in s:
                        country = s["country"]
                    elif "university" in s:
                        university = s["university"]
                    elif "center" in s:
                        center = s["center"]

                    elif (
                        "location" in s
                    ):  # aff.ParseMethod = AffiliationParseMethod.TITIPATA_API  # noqa: E501
                        location = s["location"]
                    elif (
                        "email" in s
                    ):  # aff.ParseMethod = AffiliationParseMethod.TITIPATA_API  # noqa: E501
                        email = s["email"]
                    elif (
                        "zipcode" in s
                    ):  # aff.ParseMethod = AffiliationParseMethod.TITIPATA_API  # noqa: E501
                        zipcode = s["zipcode"]

                    else:
                        print(s)
            aff = one_aff.Text

            affiliation_list.append(
                {
                    "text": aff,
                    "country": country,
                    "university": university,
                    "location": location,
                    "center": center,
                    "institute": institute,
                    "department": department,
                    "hospital": hospital,
                    "email": email,
                    "zipcode": zipcode,
                }
            )

    else:
        aff = None

    return {"fullname": fullname, "affiliations": affiliation_list}

def shorten_name_from_first_last(full_name: str) -> str:
    """
    Convert a full name from the format "[First Name], [Last Name]"
    to a shortened format "[Last Name], [F.]" where F is the first initial
    of the first name.

    Parameters:
        full_name (str): A string in the format "FirstName, LastName".

    Returns:
        str: The name in shortened format "LastName, F."

    Example:
        >>> shorten_name_from_first_last("John, Smith")
        'Smith, J.'
    """
    first_name, last_name = [part.strip() for part in full_name.split(',')]
    return f"{last_name}, {first_name[0]}."

def shorten_name_from_last_first(full_name: str) -> str:
    """
    Convert a full name from the format "[Last Name], [First Name]"
    to a shortened format "[Last Name], [F.]" where F is the first initial
    of the first name.

    Parameters:
        full_name (str): A string in the format "LastName, FirstName".

    Returns:
        str: The name in shortened format "LastName, F."

    Example:
        >>> shorten_name_from_last_first("Smith, John")
        'Smith, J.'
    """
    try:
        last_name, first_name = [part.strip() for part in full_name.split(',')]
    except Exception as e: # ToDo error_name_export_in_dataset
        last_name = "Error"
        first_name = str(e)


    return f"{last_name}, {first_name[0]}."


def _converter_authors_to_short(article: Article):
    author_fullname_list = []

    # Check SourceBank
    if article.SourceBank is None:
        # This is Pubmed
        article.SourceBank = SourceBankType.PUBMED

    if article.SourceBank == SourceBankType.PUBMED:
        if article.Authors is not None:
            for author in article.Authors:
                if author.ForeName is not None:
                    a = shorten_name_from_last_first(f"{author.LastName}, {author.ForeName}")
                else:
                    a = author.FullName
                author_fullname_list.append(a)


    elif article.SourceBank == SourceBankType.ARXIV:
        pass
        # json_article = _json_converter_01_arxiv(article)
    elif article.SourceBank == SourceBankType.WOS:
        if article.Authors is not None:
            for author in article.Authors:
                author_fullname_list.append(f"{author.FullName}.")


    elif article.SourceBank == SourceBankType.SCOPUS:
        if article.Authors is not None:
            for author in article.Authors:
                author_fullname_list.append(author.FullName)

    elif article.SourceBank == SourceBankType.IEEE:
        if article.Authors is not None:
            for author in article.Authors:
                author_fullname_list.append(author.FullName)

    elif article.SourceBank == SourceBankType.UNKNOWN:
        pass
    elif article.SourceBank == SourceBankType.GOOGLESCHOLAR:
        if article.Authors is not None:
            for author in article.Authors:
                author_fullname_list.append(shorten_name_from_last_first(author.FullName))
    elif article.SourceBank == SourceBankType.EMBASE:
        if article.Authors is not None:
            for author in article.Authors:
                author_fullname_list.append(author.FullName)
    elif article.SourceBank == SourceBankType.ACM:
        if article.Authors is not None:
            for author in article.Authors:
                author_fullname_list.append(author.FullName)
    else:
        raise NotImplementedError

    return author_fullname_list