from triplea.schemas.article import AffiliationParseMethod, Article, SourceBankType
import triplea.client.affiliation_parser as client_affiliation_parser
from triplea.service.graph.extract import Emmanuel
# from triplea.utils.general import print_pretty_dict


def _get_affiliation_integrated_from_pubmed(article: Article):
    aff_list = []
    if article.Authors is not None:
        for a in article.Authors:
            if a.Affiliations is not None:
                for aff in a.Affiliations:
                    # aff_list.append({"Text" : aff})
                    aff_list.append(aff.Text)
    return Emmanuel(aff_list)


def _get_affiliation_integrated_from_wos_scopus(article: Article):
    aff_list = []
    if article.OreginalArticle is not None:
        if "file" in article.OreginalArticle:
            last_e = ""
            for num in range(0, len(article.OreginalArticle["file"])):
                line = article.OreginalArticle["file"][num]
                element_value = line.split("  - ")
                e = element_value[0]
                # ------------------------------Check for line without tag (in endnote)
                if len(element_value) == 2:
                    v = str.replace(element_value[1], "\n", "").strip()
                    last_e = e
                    if v.__contains__("\n"):
                        print("wow")
                else:  # len split is 1
                    if last_e == "AD":  # First Line
                        # aff_list.append({"Text" : v})
                        aff_list.append(v)

                    v = ""
                # ------------------------------Check for line without tag (in endnote)
                if e == "AD":
                    # aff_list.append({"Text" : v})
                    aff_list.append(v)
    return Emmanuel(aff_list)


def _affiliation_mining_titipata_in_list(aff_list):
    if aff_list is None:
        return None
    structural_aff_list = []
    for aff in aff_list:
        # affl_normal_text = aff['Text'].replace("/", " ")
        affl_normal_text = aff.replace("/", " ")

        affl = client_affiliation_parser.parse_affiliation(affl_normal_text)
        loc = []
        if "country" in affl:
            loc.append({"country": affl["country"]})
        if "department" in affl:
            loc.append({"department": affl["department"]})
        if "email" in affl:
            loc.append({"email": affl["email"]})
        if "institution" in affl:
            loc.append({"institution": affl["institution"]})
        if "location" in affl:
            loc.append({"location": affl["location"]})
        if "zipcode" in affl:
            loc.append({"zipcode": affl["zipcode"]})

        # loc.append({"method" : "Titipata"})
        structural_aff_list.append(
            {
                "Text": aff,
                "ParseMethod": AffiliationParseMethod.TITIPATA_API,
                "Structural": loc,
            }
        )
        # aff['ParseMethod'] = AffiliationParseMethod.TITIPATA_API
        # aff['Structural'] = loc

    return structural_aff_list


def affiliation_mining_titipata_integration(article: Article):
    # this is dispatcher function
    if article.SourceBank is None:
        # This is Pubmed
        # updated_article = _get_citation_pubmed(article)
        aff_list = _get_affiliation_integrated_from_pubmed(article)
    elif article.SourceBank == SourceBankType.PUBMED:
        # updated_article = _get_citation_pubmed(article)
        aff_list = _get_affiliation_integrated_from_pubmed(article)
    elif article.SourceBank == SourceBankType.ARXIV:
        aff_list = None  # I haven't found a way to do it yet
    elif article.SourceBank == SourceBankType.WOS:
        aff_list = _get_affiliation_integrated_from_wos_scopus(article)
    elif article.SourceBank == SourceBankType.SCOPUS:
        aff_list = _get_affiliation_integrated_from_wos_scopus(article)
    elif article.SourceBank == SourceBankType.IEEE:
        aff_list = _get_affiliation_integrated_from_wos_scopus(article)
    elif article.SourceBank == SourceBankType.UNKNOWN:
        aff_list = _get_affiliation_integrated_from_wos_scopus(article)
    elif article.SourceBank == SourceBankType.GOOGLESCHOLAR:
        aff_list = _get_affiliation_integrated_from_wos_scopus(article)
    elif article.SourceBank == SourceBankType.EMBASE:
        aff_list = _get_affiliation_integrated_from_wos_scopus(article)
    elif article.SourceBank == SourceBankType.ACM:
        aff_list = _get_affiliation_integrated_from_wos_scopus(article)
    else:
        raise NotImplementedError

    new_aff_list = _affiliation_mining_titipata_in_list(aff_list)
    article.AffiliationIntegration = new_aff_list
    article.FlagAffiliationMining = 1
    return article
