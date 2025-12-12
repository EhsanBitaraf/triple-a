import logging
from datetime import datetime
from typing import Optional, Dict, Any

from triplea.client.altmetric import get_altmetric
from triplea.schemas.article import Article
from urllib.parse import quote_plus

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def model_altmetric_by_doi(article: Article, overwrite: bool = False) -> Optional[Article]:
    """Enrich an article with Altmetric data using its DOI.
    
    Fetches Altmetric data for an article using its DOI and adds it to the article's
    EnrichedData field. If Altmetric data already exists, it will only be updated
    if overwrite is True.
    
    Args:
        article (Article): The article object to enrich with Altmetric data.
        overwrite (bool, optional): If True, overwrites existing Altmetric data.
            Defaults to False.
    
    Returns:
        Optional[Article]: The enriched article object if successful, None if:
            - Article has no DOI
            - Altmetric data already exists and overwrite is False
            - Error occurred during data fetch
    
    Examples:
        >>> article = Article(DOI="10.1038/nphys1170")
        >>> enriched = model_altmetric_by_doi(article)
        >>> if enriched:
        ...     print("Article enriched successfully")
        
        >>> # Overwrite existing data
        >>> enriched = model_altmetric_by_doi(article, overwrite=True)
    
    Raises:
        Exception: If get_altmetric fails to fetch data from the API.
    """

    if not isinstance(article, Article):
        logger.error("Input 'article' must be an instance of Article; got %r", type(article))
        raise ValueError("The 'article' parameter must be an instance of Article.")

    if article.DOI is None:
        logger.debug(f"Article has no DOI, skipping Altmetric enrichment")
        return None
    
    # Initialize EnrichedData if it doesn't exist
    if article.EnrichedData is None:
        article.EnrichedData = {}
    
    try:
        if overwrite:
            # Fetch Altmetric data using the article's DOI
            logger.debug(f"Fetching Altmetric data for DOI: {article.DOI}")
            data = get_altmetric(quote_plus(article.DOI), id_type="doi")
        else:
            if 'altmetric' in article.EnrichedData:
                logger.debug(f"Altmetric data already exists for DOI: {article.DOI}, skipping")
                return None
            else:
                logger.debug(f"Fetching Altmetric data for DOI: {article.DOI}")
                data = get_altmetric(quote_plus(article.DOI), id_type="doi")



        
        if data is None:
            logger.warning(f"No Altmetric data found for DOI: {article.DOI}")
            return None
        

        
        # Check if Altmetric data already exists
        if 'altmetric' in article.EnrichedData:
            if overwrite:
                logger.info(f"Overwriting existing Altmetric data for DOI: {article.DOI}")
                article.EnrichedData['altmetric'] = {
                    "date": datetime.now(),
                    "data": data
                }
                return article
            else:
                logger.debug(f"Altmetric data already exists for DOI: {article.DOI}, skipping")
                return None
        else:
            # Add new Altmetric data
            logger.info(f"Adding Altmetric data for DOI: {article.DOI}")
            article.EnrichedData['altmetric'] = {
                "date": datetime.now(),
                "data": data
            }
            return article
            
    except Exception as e:
        logger.error(f"Error fetching Altmetric data for DOI {article.DOI}: {str(e)}")
        raise


