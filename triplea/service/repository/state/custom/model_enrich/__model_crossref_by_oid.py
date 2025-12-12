import logging
from datetime import datetime
from typing import Optional
from triplea.client.crossref import crossref_by_doi
from triplea.schemas.article import Article

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def model_crossref_by_oid(article: Article, overwrite: bool = False) -> Optional[Article]:
    """Fetch and attach Crossref metadata for an `Article` identified by DOI.

    This function attempts to enrich the provided `Article` instance by fetching
    metadata from Crossref using the article's DOI and placing the result under
    `article.EnrichedData['crossref']`. If enrichment already exists and
    `overwrite` is `False`, the function performs no mutation and returns `None`.

    Behavior summary:
        1. Validates that `article` is an instance of `Article`.
        2. Returns `None` immediately if the `Article` has no DOI.
        3. Calls Crossref using `crossref_by_doi(article.DOI, id_type="doi")`.
        4. If no data is returned, logs a warning and returns `None`.
        5. Initializes `article.EnrichedData` as a dict if missing.
        6. Writes (or overwrites, if `overwrite=True`) the `'crossref'` entry:
           `{"date": datetime.now(), "data": <crossref-payload>}`.
        7. Returns the mutated `Article` on successful write; otherwise `None`.

    Args:
        article (Article):
            The target article to be enriched. Must have a `DOI` attribute and an
            `EnrichedData` mapping-like attribute (or `None`) compatible with dict
            assignment.
        overwrite (bool, optional):
            Whether to overwrite existing `'crossref'` enrichment if present.
            Defaults to `False`.

    Returns:
        Optional[Article]:
            - The same `Article` instance (mutated in place) when enrichment
              is newly added or overwritten.
            - `None` if no enrichment was performed (e.g., no DOI, no Crossref
              data found, or enrichment existed and `overwrite=False`).

    Raises:
        ValueError:
            If `article` is not an instance of `Article`.
        Exception:
            Propagates any unexpected exceptions raised during the Crossref fetch
            or while mutating `article.EnrichedData`. The exact exception type
            depends on the underlying failure (e.g., network issues, schema
            mismatches).

    Examples:
        Basic usage (add Crossref data if missing):

        >>> from triplea.schemas.article import Article
        >>> a = Article(DOI="10.1038/s41586-020-2649-2", EnrichedData=None)
        >>> updated = model_crossref_by_oid(a)  # returns `a` if data was fetched
        >>> isinstance(updated, Article)
        True
        >>> 'crossref' in a.EnrichedData
        True

        Skipping when Crossref data exists:

        >>> a = Article(DOI="10.1038/s41586-020-2649-2",
        ...             EnrichedData={'crossref': {'date': datetime.now(), 'data': {'title': '...'}}})
        >>> result = model_crossref_by_oid(a)  # overwrite=False by default
        >>> result is None
        True  # No changes made

        Forcing an overwrite:

        >>> forced = model_crossref_by_oid(a, overwrite=True)
        >>> isinstance(forced, Article)
        True
        >>> 'crossref' in forced.EnrichedData
        True  # 'crossref' updated with fresh fetch and a new timestamp

        Handling missing DOI:

        >>> b = Article(DOI=None, EnrichedData=None)
        >>> model_crossref_by_oid(b) is None
        True  # Nothing to do; DOI is required

    """
    # Validate input type early; this makes failures explicit and easier to debug
    # for callers that may inadvertently pass the wrong object.
    if not isinstance(article, Article):
        logger.error("Input 'article' must be an instance of Article; got %r", type(article))
        raise ValueError("The 'article' parameter must be an instance of Article.")

    # A DOI is required to perform the Crossref lookup. If absent, we exit early.
    if article.DOI is None:
        logger.debug(f"Article has no DOI, skipping Crossref enrichment")
        return None
    
    try:
        if overwrite:
            # Fetch Crossref data using the article's DOI
            logger.debug(f"Fetching Crossref data for DOI: {article.DOI}")
            data = crossref_by_doi(article.DOI)
        else:
            if 'crossref' in article.EnrichedData:
                logger.debug(f"crossref data already exists for DOI: {article.DOI}, skipping")
                return None         
            else:
                logger.debug(f"Fetching Crossref data for DOI: {article.DOI}")
                data = crossref_by_doi(article.DOI)                       

        
        # Crossref did not return a payload; nothing to enrich.
        if data is None:
            logger.warning(f"No Crossref data found for DOI: {article.DOI}")
            return None
        
        # Ensure EnrichedData is initialized to a dict before writing.
        if article.EnrichedData is None:
            article.EnrichedData = {}
        
        # If Crossref data already exists, either overwrite or skip based on flag.
        if 'crossref' in article.EnrichedData:
            if overwrite:
                logger.info(f"Overwriting existing Crossref data for DOI: {article.DOI}")
                article.EnrichedData['crossref'] = {
                    "date": datetime.now(),
                    "data": data
                }
                return article
            else:
                logger.debug(f"crossref data already exists for DOI: {article.DOI}, skipping")
                return None
        else:
            # Add new Crossref data (first-time enrichment).
            logger.info(f"Adding Crossref data for DOI: {article.DOI}")
            article.EnrichedData['crossref'] = {
                "date": datetime.now(),
                "data": data
            }
            return article
            
    except Exception as e:
        # Log and re-raise to preserve the original stack trace for the caller.
        logger.error(f"Error fetching Crossref data for DOI {article.DOI}: {str(e)}")
        raise




def model_crossref_by_oid_without_pmid(article: Article, overwrite: bool = False) -> Optional[Article]:
    if not isinstance(article, Article):
        logger.error("Input 'article' must be an instance of Article; got %r", type(article))
        raise ValueError("The 'article' parameter must be an instance of Article.")

    if article.DOI is None:
        logger.debug(f"Article has no DOI, skipping Crossref enrichment")
        return None

    if article.PMID is not None:
        logger.debug(f"Article has PMID, skipping Crossref enrichment")
        return None
    
    try:
        # Fetch Crossref data using the article's DOI
        logger.debug(f"Fetching Crossref data for DOI: {article.DOI}")
        data = crossref_by_doi(article.DOI)
        
        if data is None:
            logger.warning(f"No Crossref data found for DOI: {article.DOI}")
            return None
        
        # Initialize EnrichedData if it doesn't exist
        if article.EnrichedData is None:
            article.EnrichedData = {}
        
        # Check if Altmetric data already exists
        if 'crossref' in article.EnrichedData:
            if overwrite:
                logger.info(f"Overwriting existing Crossref data for DOI: {article.DOI}")
                article.EnrichedData['crossref'] = {
                    "date": datetime.now(),
                    "data": data
                }
                return article
            else:
                logger.debug(f"crossref data already exists for DOI: {article.DOI}, skipping")
                return None
        else:
            # Add new Crossref data
            logger.info(f"Adding Crossref data for DOI: {article.DOI}")
            article.EnrichedData['crossref'] = {
                "date": datetime.now(),
                "data": data
            }
            return article
            
    except Exception as e:
        logger.error(f"Error fetching Crossref data for DOI {article.DOI}: {str(e)}")
        raise
