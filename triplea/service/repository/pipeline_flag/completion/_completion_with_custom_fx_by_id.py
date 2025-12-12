import logging
from triplea.schemas.article import Article
import triplea.service.repository.persist as persist

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def _get_article_for_completion_by_id(article_id):
    """
    Retrieve and construct an `Article` object from persistent storage using its ID.

    This function queries the underlying persistence layer to fetch raw article data
    by its unique identifier, then parses and instantiates it into an `Article` model
    object. It performs validation, structured error handling, and detailed logging
    to help diagnose retrieval or parsing issues.

    Args:
        article_id (str | int): The unique identifier of the article to retrieve.
            Must be a non-empty string or a non-negative integer.

    Returns:
        Article: A fully constructed `Article` object containing the article data
        retrieved from persistence.

    Raises:
        ValueError: 
            - If `article_id` is None or invalid.
            - If the article could not be retrieved from persistence storage.
            - If the retrieved data could not be parsed into an `Article` object.

    Example:
        >>> from triplea.schemas.article import Article
        >>> article = _get_article_for_completion_by_id("12345")
        >>> isinstance(article, Article)
        True

    Notes:
        - This function is typically used internally as a helper for completion
          workflows that depend on article metadata or content.
        - It uses logging to record both retrieval and parsing errors for debugging.
    """
    # Validate input ID early to avoid unnecessary database or persistence operations
    if article_id is None:
        logger.error("article_id is None.")  # Log error for diagnostic tracking
        raise ValueError(
            "article_id must be a non-empty string or a non-negative integer."
        )

    try:
        # Attempt to fetch article data from the persistence repository
        article_data = persist.get_article_by_id(article_id)
    except Exception as e1:        
        # Log and re-raise with contextual error message for clarity
        logger.error(f"Error getting article by {article_id}: {str(e1)}")
        raise ValueError(f"Failed to get article by ({article_id})") from e1 
      
    try:
        # Attempt to parse the raw data into an Article schema object
        # Using `.copy()` to avoid mutating the original data dictionary
        article = Article(**article_data.copy())
    except Exception as e2:
        # Log and re-raise parsing errors with detailed context
        logger.error(f"Error parsing article ({article_id}): {str(e2)}")
        raise ValueError(f"Failed to parse article ({article_id})") from e2
    
    # Return the successfully parsed and validated Article object
    return article

      

def _save_updated_article(updated_article:Article, article_id):
    try:
        if updated_article is not None:
            persist.update_article_by_id(updated_article, article_id)
            logger.info(f"Article ({article_id}) updated.")
        else:
            logger.debug(f"Article ({article_id}) does not need to be updated.")
    except Exception as e:
        logger.error(f"Error in saving article ID {article_id}: {str(e)}")
        raise 

def completion_with_custom_fx_by_id(article_id, fx):
    try:
        article = _get_article_for_completion_by_id(article_id)
        logger.debug(f"Completion process run on article {article_id} with custom method `{fx.__name__}`")

        # ----- Change Article Based on model completion ------
        updated_article = fx(article)
        # ----- Change Article Based on model completion ------

        _save_updated_article(updated_article, article_id)
    except Exception as e:
        logger.error(f"Error in saving article ID {article_id}: {str(e)}")
        raise 