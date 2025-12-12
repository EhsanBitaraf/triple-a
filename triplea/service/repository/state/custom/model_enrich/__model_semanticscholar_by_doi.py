
import logging
from datetime import datetime
from typing import Optional
from triplea.client.semanticscholar import semanticscholar_by_doi
from triplea.schemas.article import Article

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def model_semanticscholar_by_doi(article: Article, overwrite: bool = False) -> Optional[Article]:
        # Validate input type early; this makes failures explicit and easier to debug
    # for callers that may inadvertently pass the wrong object.
    if not isinstance(article, Article):
        logger.error("Input 'article' must be an instance of Article; got %r", type(article))
        raise ValueError("The 'article' parameter must be an instance of Article.")

    # A DOI is required to perform the semanticscholar lookup. If absent, we exit early.
    if article.DOI is None:
        logger.debug(f"Article has no DOI, skipping semanticscholar enrichment")
        return None
    
    try:
        if overwrite:
            # Fetch semanticscholar data using the article's DOI
            logger.debug(f"Fetching semanticscholar data for DOI: {article.DOI}")
            data = semanticscholar_by_doi(article.DOI)
        else:
            if 'semanticscholar' in article.EnrichedData:
                logger.debug(f"semanticscholar data already exists for DOI: {article.DOI}, skipping")
                return None         
            else:
                logger.debug(f"Fetching semanticscholar data for DOI: {article.DOI}")
                data = semanticscholar_by_doi(article.DOI)                       

        
        # semanticscholar did not return a payload; nothing to enrich.
        if data is None:
            logger.warning(f"No semanticscholar data found for DOI: {article.DOI}")
            return None
        
        # Ensure EnrichedData is initialized to a dict before writing.
        if article.EnrichedData is None:
            article.EnrichedData = {}
        
        # If semanticscholar data already exists, either overwrite or skip based on flag.
        if 'semanticscholar' in article.EnrichedData:
            if overwrite:
                logger.info(f"Overwriting existing semanticscholar data for DOI: {article.DOI}")
                article.EnrichedData['semanticscholar'] = {
                    "date": datetime.now(),
                    "data": data
                }
                return article
            else:
                logger.debug(f"semanticscholar data already exists for DOI: {article.DOI}, skipping")
                return None
        else:
            # Add new semanticscholar data (first-time enrichment).
            logger.info(f"Adding semanticscholar data for DOI: {article.DOI}")
            article.EnrichedData['semanticscholar'] = {
                "date": datetime.now(),
                "data": data
            }
            return article
            
    except Exception as e:
        # Log and re-raise to preserve the original stack trace for the caller.
        logger.error(f"Error fetching semanticscholar data for DOI {article.DOI}: {str(e)}")
        raise

