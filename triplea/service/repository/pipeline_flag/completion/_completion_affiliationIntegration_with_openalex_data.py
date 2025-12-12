from triplea.service.repository.pipeline_flag.completion._completion_with_custom_fx_by_id import _get_article_for_completion_by_id, _save_updated_article
import logging
from triplea.schemas.article import AffiliationParseMethod, Article
from triplea.service.repository.state.custom.affiliation_mining_multiple_parser import _affiliation_mining_multiple_parser_in_list


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def _fx(article:Article):
    if not (article.AffiliationIntegration is None or article.AffiliationIntegration == []):
        logger.debug(f"Article alredy has AffiliationIntegration.")
        return None
    
    if article.EnrichedData is None:
        logger.debug(f"EnrichedData not exist. You must use go_get_enrich_data before this.")
        return None

    if 'openalex' not in article.EnrichedData:
        logger.debug(f"OpenAlex data not exist in EnrichedData.")
        return None

    # Parse OpenAlex affiliation
    if 'authorships' in article.EnrichedData['openalex']['data']:
        al = article.EnrichedData['openalex']['data']['authorships']
        my_affiliation_list = []
        for a in al:
            if 'raw_affiliation_strings' in a:
                if isinstance(a['raw_affiliation_strings'],list):
                    my_affiliation_list.append(a['raw_affiliation_strings'][0])
                elif isinstance(a['raw_affiliation_strings'],str):
                    my_affiliation_list.append(a['raw_affiliation_strings'])

        ## Get structure data from affiliation parsing service
        parsed_aff_list = _affiliation_mining_multiple_parser_in_list(
            my_affiliation_list,
            AffiliationParseMethod.REGEX_API)
        logger.debug(f"Parse list of affiliation with service.")
        article.AffiliationIntegration = parsed_aff_list
        article.FlagAffiliationMining = 1
        return article
    else:
        logger.debug(f"OpenAlex data has no authorships.")
        return None

def completion_affiliationIntegration_with_openalex_data(article_id):
    try:
        article = _get_article_for_completion_by_id(article_id)
        logger.debug(f"Completion process run on article {article_id} with custom method `completion_affiliationIntegration_with_openalex_data`")

        # ----- Change Article Based on model completion ------
        updated_article = _fx(article)
        # ----- Change Article Based on model completion ------

        _save_updated_article(updated_article ,article_id)
    except Exception as e:
        logger.error(f"Error in saving article ID {article_id}: {str(e)}")
        raise 


