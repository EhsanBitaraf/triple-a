"""
This is new API
"""


from triplea.schemas.article import AffiliationParseMethod, Article
from triplea.service.repository.state.custom.affiliation_mining_titipata_integration import _get_affiliation_list_from_all_bank
# import triplea.client.affiliation_parser_multiple as client_affiliation_parser
from triplea.client.affiliation_parser_multiple import parse_affiliation_multiple

def _affiliation_mining_multiple_parser_in_list(aff_list,
                                                method:AffiliationParseMethod):
    if aff_list is None:
        return None
    structural_aff_list = []
    for aff in aff_list:
        # affl_normal_text = aff['Text'].replace("/", " ")
        affl_normal_text = aff.replace("/", " ")

        affl = parse_affiliation_multiple(
            affl_normal_text,int(method))
        loc = []
        if "countries" in affl:
            loc.append({"country": affl["countries"]})
        if "departments" in affl:
            loc.append({"department": affl["departments"]})
        if "emails" in affl:
            loc.append({"email": affl["emails"]})
        if "institutes" in affl:
            loc.append({"institution": affl["institutes"]})
        if "faculties" in affl:
            loc.append({"faculty": affl["faculties"]})
        if "zipcode" in affl:
            loc.append({"zipcode": affl["postcodes"]})
        if "universities" in affl:
            loc.append({"university": affl["universities"]})
        if "government_entities" in affl:
            loc.append({"government_entity": affl["government_entities"]})
        if "cities" in affl:
            loc.append({"city": affl["cities"]})

        structural_aff_list.append(
            {
                "Text": aff,
                "ParseMethod": int(method),
                "Structural": loc,
            }
        )
        # aff['ParseMethod'] = AffiliationParseMethod.TITIPATA_API
        # aff['Structural'] = loc

    return structural_aff_list


def affiliation_mining_regex_integration(article: Article):
    aff_list = _get_affiliation_list_from_all_bank (article)


    new_aff_list = _affiliation_mining_multiple_parser_in_list(
        aff_list,
        AffiliationParseMethod.REGEX_API)
    article.AffiliationIntegration = new_aff_list
    article.FlagAffiliationMining = 1
    return article