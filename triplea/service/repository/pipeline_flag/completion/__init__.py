import logging

from triplea.config.settings import SETTINGS
import triplea.service.repository.persist as persist
from triplea.utils.general import get_tqdm
from triplea.service.repository.pipeline_flag.completion._completion_with_custom_fx_by_id import completion_with_custom_fx_by_id
from triplea.service.repository.pipeline_flag.completion._completion_affiliationIntegration_with_openalex_data import completion_affiliationIntegration_with_openalex_data



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

            logger.debug(f"Completion for article {article_id}")
            # Update progress bar description
            if bar:
                bar.set_description(f"Completion for article {article_id}")
                bar.update(1)

            # Process article based on method
            if method_fx is None:
                if method_name == "completion_affiliationIntegration_with_openalex_data":
                    completion_affiliationIntegration_with_openalex_data(article_id)
                else:
                    logger.error("Method name is not recognized.")
                    raise Exception()
            else:
                
                completion_with_custom_fx_by_id(article_id, method_fx)

        except Exception as e:
            logger.error(f"Unexpected error processing article ID {article_id}: {str(e)}")
            continue

    # Final refresh and cleanup
    persist.refresh()
    if bar:
        bar.close()
    logger.info("Completion process completed.")



# Define function

__all__ = [
    "completion_with_custom_fx_by_id",
    "completion_affiliationIntegration_with_openalex_data",

]