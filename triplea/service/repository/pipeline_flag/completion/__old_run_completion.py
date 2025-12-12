import logging
from typing import Optional
from triplea.config.settings import SETTINGS
from triplea.schemas.article import Article
import triplea.service.repository.persist as persist
from triplea.utils.general import get_tqdm

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def run_completion(
    method_name,
    method_fx = None,
    proccess_bar: bool = True,
) -> None:

    # Input validation
    if method_name is None and method_fx is None:
        logger.error("one of Parameter 'method_name' or 'method_fx' must have value.")
        raise ValueError("one of Parameter 'method_name' or 'method_fx' must have value.")

    max_refresh_point = SETTINGS.AAA_CLI_ALERT_POINT
    l_id = persist.get_all_article_id_list()
    total_article = len(l_id)
    logger.info(f"{total_article} Article(s) in completion process")

    # Initialize progress bar if enabled
    if proccess_bar:
        tqdm = get_tqdm()
        bar = tqdm(total=total_article, desc="Processing")
    else:
        bar = None  # No progress bar

    refresh_point = 0
    processed_count = 0

    for article_id in l_id:
        try:
            processed_count += 1
            # Refresh repository at intervals to prevent memory issues
            if refresh_point == max_refresh_point:
                refresh_point = 0
                persist.refresh()
                remaining = total_article - processed_count
                logger.info(f"{remaining} article(s) remaining for process")
            else:
                refresh_point += 1

            # Fetch and validate article
            article_data = persist.get_article_by_id(article_id)

            try:
                article = Article(**article_data.copy())
            except Exception as e:
                logger.error(f"Error parsing article ID {article_id}: {str(e)}")
                raise ValueError(f"Failed to parse article ID {article_id}") from e

            logger.debug(f"Completion for article {article_id}")
            # Update progress bar description
            if bar:
                bar.set_description(f"Completion for article {article_id}")
                bar.update(1)

            # Process article based on method
            if method_fx is None:
                if method_fx == "":
                    pass
                else:
                    logger.error(f"Method name `{article_id}` is not recognized.")
                    raise
            else:
                logger.debug(f"Completion process run on article {article_id} with custom method `{method_fx.__name__}`")
                updated_article = method_fx(article)
            
            if updated_article is not None:
                persist.update_article_by_id(updated_article, article_id)
                logger.info(f"Article ({article_id}) updated.")



        except Exception as e:
            logger.error(f"Unexpected error processing article ID {article_id}: {str(e)}")
            continue

    # Final refresh and cleanup
    persist.refresh()
    if bar:
        bar.close()
    logger.info("Completion process completed.")