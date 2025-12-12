
# from triplea.service.click_logger import logger
from triplea.schemas.article import Article
import triplea.service.repository.state as state_manager
import triplea.service.repository.persist as persist


import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def move_article_state_forward_by_id(id):
    a = persist.get_article_by_id(id)
    try:
        article = Article(**a.copy())
    except Exception as e1:
        logger.error(f"Error in parsing article with ID = {id} : {e1}" , exc_info=True)
        raise
    
    if article.State is None:
        article.State = 0

    current_state = article.State

    
    if current_state is None:
        updated_article = state_manager.expand_details(article)

    elif current_state == 0:  # Next state: get article details from pubmed
        updated_article = state_manager.expand_details(article)

    elif current_state == 1:  # Next state: Extract Data
        updated_article = state_manager.parsing_details(article)

    elif current_state == -1:  # Error in State 0 Next state: 1
        updated_article = state_manager.parsing_details(article)

    elif current_state == 2:  # Next state: Get Citation
        updated_article = state_manager.get_citation(article)

    elif current_state == -2:  # Next state: Get Citation
        updated_article = state_manager.get_citation(article)

    elif current_state == 3:  # Next state: Get Full Text
        updated_article = state_manager.get_full_text(article)

    elif current_state == -3:  # Next state: Get Full Text
        updated_article = state_manager.get_full_text(article)

    elif current_state == 4:  # Next state: Convert Full Text
        updated_article = state_manager.convert_full_text2string(
            article
        )

    elif current_state == -4:  # Next state: Convert Full Text
        updated_article = state_manager.convert_full_text2string(
            article
        )

    else:
        logger.error(f"undefine current state in article with ID = {id}")
        raise Exception(f"undefine current state in article with ID = {id}")
    
    try:
        persist.update_article_by_id(updated_article, id)
        logger.debug(f"article {id} update and saved.")
    except Exception as e2:
        logger.error(f"Error in saving article with ID = {id} : {e2}" , exc_info=True)
        raise 
    


