import logging
from datetime import datetime
from typing import Optional, Dict, Any

from triplea.client.altmetric import get_altmetric
import triplea.service.repository.persist as persist
from triplea.config.settings import SETTINGS
from triplea.utils.general import print_error, get_tqdm
from triplea.schemas.article import Article

from triplea.service.repository.state.custom.model_enrich import (
     model_altmetric_by_doi,
     model_crossref_by_oid,
     model_crossref_by_oid_without_pmid,
     model_openalex_by_doi,
     model_semanticscholar_by_doi

)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def go_get_enrich_data(model: str,
                       model_fx = None,
                      overwrite: bool = False) -> None:

    # Get the refresh point from settings (how often to refresh DB connection)
    max_refresh_point = SETTINGS.AAA_CLI_ALERT_POINT
    
    try:
        # Fetch all article IDs from the database
        l_id = persist.get_all_article_id_list()
        total_article = len(l_id)
        
        if total_article == 0:
            logger.warning("No articles found in the database")
            return
        
        logger.info(f"Starting enrichment for {total_article} article(s) using model: {model}")
        
        # Initialize progress tracking
        n = 0
        refresh_point = 0
        
        # Create progress bar
        tqdm = get_tqdm()
        bar = tqdm(total=len(l_id), desc="Processing articles")
        
        # Process each article
        for id in l_id:
            try:
                n += 1
                bar.set_description(f" article(s) {id} process ...")
                bar.update(1)
                
                # Periodically refresh database connection to avoid timeouts
                if refresh_point == max_refresh_point:
                    refresh_point = 0
                    persist.refresh()
                    logger.debug(f"Database refreshed. {total_article - n} article(s) remaining")
                else:
                    refresh_point += 1
                
                # Retrieve article from database
                a = persist.get_article_by_id(id)
                
                if a is None:
                    logger.warning(f"Article with ID {id} not found in database")
                    raise Exception (f"Article with ID {id} not found in database")
                
                # Parse article object
                try:
                    article = Article(**a.copy())
                except Exception as e:
                    logger.error(f"Error parsing article with ID {id}: {str(e)}")
                    raise

                # Apply custom enrichment model
                if model_fx is not None:
                    model = "custom_model"
                    updated_article = model_fx(article, overwrite=overwrite)

                
                # Apply enrichment model
                if model == "custom_model":
                    pass
                
                elif model == "altmetric_by_doi":
                    updated_article = model_altmetric_by_doi(article,
                                                             overwrite=overwrite)
                
                elif model == "crossref_by_oid":
                    updated_article = model_crossref_by_oid(article,
                                                            overwrite=overwrite)

                elif model == "crossref_by_oid_without_pmid":
                    updated_article = model_crossref_by_oid_without_pmid(article,
                                                                          overwrite=overwrite)

                elif model == "openalex_by_doi":
                    updated_article = model_openalex_by_doi(article,
                                                             overwrite=overwrite)
                    
                elif model == "semanticscholar_by_doi":
                    updated_article = model_semanticscholar_by_doi(article,
                                                                    overwrite=overwrite)


                else:
                    raise ValueError(f"Model '{model}' not recognized.")


                # Update article in database 
                if updated_article is not None:
                    persist.update_article_by_id(updated_article, id)
                    logger.debug(f"Article {id} successfully enriched and updated")
                else:
                    logger.debug(f"Article {id} skipped (no DOI or already enriched)")
                
                
            except Exception as e:
                logger.error(f"Error processing article {id}: {str(e)}")
                print_error()
                bar.update(1)
                continue
        
        # Final database refresh and cleanup
        persist.refresh()
        bar.close()
        logger.info(f"Enrichment process completed. Processed {total_article} article(s)")
        
    except Exception as e:
        logger.error(f"Fatal error in enrichment process: {str(e)}")
        raise


    