
import logging
from datetime import datetime
from typing import Optional
from triplea.client.openalex import openalex_by_doi
from triplea.schemas.article import Article

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def model_openalex_by_doi(article: Article, overwrite: bool = False) -> Optional[Article]:
        # Validate input type early; this makes failures explicit and easier to debug
    # for callers that may inadvertently pass the wrong object.
    if not isinstance(article, Article):
        logger.error("Input 'article' must be an instance of Article; got %r", type(article))
        raise ValueError("The 'article' parameter must be an instance of Article.")

    # A DOI is required to perform the openalex lookup. If absent, we exit early.
    if article.DOI is None:
        logger.debug(f"Article has no DOI, skipping openalex enrichment")
        return None
    
    try:

        # Ensure EnrichedData is initialized to a dict before writing.
        if not isinstance(article.EnrichedData, dict):
            article.EnrichedData = {}  # guarantees it's iterable
            
        if overwrite:
            # Fetch openalex data using the article's DOI
            logger.debug(f"Fetching openalex data for DOI: {article.DOI}")
            data = openalex_by_doi(article.DOI)
        else:
            if 'openalex' in article.EnrichedData:
                logger.debug(f"openalex data already exists for DOI: {article.DOI}, skipping")
                return None         
            else:
                logger.debug(f"Fetching openalex data for DOI: {article.DOI}")
                data = openalex_by_doi(article.DOI)                       

        
        # openalex did not return a payload; nothing to enrich.
        if data is None:
            logger.warning(f"No openalex data found for DOI: {article.DOI}")
            return None
        

        
        # If openalex data already exists, either overwrite or skip based on flag.
        if 'openalex' in article.EnrichedData:
            if overwrite:
                logger.info(f"Overwriting existing openalex data for DOI: {article.DOI}")
                article.EnrichedData['openalex'] = {
                    "date": datetime.now(),
                    "data": data
                }
                return article
            else:
                logger.debug(f"openalex data already exists for DOI: {article.DOI}, skipping")
                return None
        else:
            # Add new openalex data (first-time enrichment).
            logger.info(f"Adding openalex data for DOI: {article.DOI}")
            article.EnrichedData['openalex'] = {
                "date": datetime.now(),
                "data": data
            }
            return article
            
    except Exception as e:
        # Log and re-raise to preserve the original stack trace for the caller.
        logger.error(f"Error fetching openalex data for DOI {article.DOI}: {str(e)}")
        raise

