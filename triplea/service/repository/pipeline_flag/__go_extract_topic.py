import logging
from typing import Optional
from triplea.config.settings import SETTINGS
from triplea.schemas.article import Article
import triplea.service.repository.persist as persist
import triplea.service.repository.state as state_manager
from triplea.utils.general import get_tqdm

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def go_extract_topic(
    method: str = "textrank",
    top: int = 10,
    threshold: float = 0.0,
    proccess_bar: bool = True,
) -> None:
    """Extracts topics from articles in the 'FlagExtractTopic' state using the specified method.

    This function processes articles with a specific state flag (FlagExtractTopic = 0),
    extracts topics from their abstracts using the provided method, and updates the article
    records in the repository. It includes progress tracking and error handling with logging.

    Args:
        method: The topic extraction method to use (default: "textrank").
        top: Number of top topics to extract (default: 10).
        threshold: Minimum score threshold for extracted topics (default: 0.0).
        proccess_bar: Whether to display a progress bar (default: True).

    Raises:
        ValueError: If the method is invalid or parameters are out of acceptable range.
        NotImplementedError: If an unsupported state is encountered.

    Examples:
        >>> go_extract_topic(method="textrank", top=5, threshold=0.1)
        # Processes articles using textrank, extracting top 5 topics with scores >= 0.1.
    """
    # Input validation
    if not isinstance(top, int) or top <= 0:
        logger.error("Parameter 'top' must be a positive integer.")
        raise ValueError("Parameter 'top' must be a positive integer.")
    if not isinstance(threshold, float) or threshold < 0:
        logger.error("Parameter 'threshold' must be a non-negative float.")
        raise ValueError("Parameter 'threshold' must be a non-negative float.")

    max_refresh_point = SETTINGS.AAA_CLI_ALERT_POINT
    l_id = persist.get_article_id_list_by_cstate(0, "FlagExtractTopic")
    total_article_in_current_state = len(l_id)
    logger.debug(f"{total_article_in_current_state} Article(s) in FlagExtractTopic state 0")

    # Initialize progress bar if enabled
    if proccess_bar:
        tqdm = get_tqdm()
        bar = tqdm(total=total_article_in_current_state, desc="Processing")
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
                remaining = total_article_in_current_state - processed_count
                logger.info(f"{remaining} article(s) remaining for topic extraction")
                if bar:
                    bar.set_description(f"{remaining} article(s) remaining")
                    bar.update(max_refresh_point)

            else:
                refresh_point += 1

            # Fetch and validate article
            article_data = persist.get_article_by_id(article_id)
            if article_data is None:
                logger.error(f"Article with ID {article_id} not found.")
                if bar:
                    bar.update(1)
                continue

            try:
                updated_article = Article(**article_data.copy())
            except Exception as e:
                logger.error(f"Error parsing article ID {article_id}: {str(e)}")
                raise ValueError(f"Failed to parse article ID {article_id}") from e

            # Get current state
            current_state: Optional[int] = getattr(updated_article, "FlagExtractTopic", None)
            if current_state is None:
                current_state = 0  # Default to unprocessed state

            # Update progress bar description
            if bar:
                bar.set_description(f"Extracting topics for article {article_id}")
                bar.update(1)

            # Process article based on state
            if current_state in [None, -1, 0]:
                try:
                    updated_article = state_manager.extract_topic_abstract(
                        updated_article, method, top, threshold
                    )
                    updated_article.FlagExtractTopic = 1  # Mark as processed
                    persist.update_article_by_id(updated_article, article_id)
                except Exception as e:
                    logger.error(f"Topic extraction failed for article ID {article_id}: {str(e)}")
                    updated_article.FlagExtractTopic = -1  # Mark as failed
                    persist.update_article_by_id(updated_article, article_id)
                    persist.refresh()
                    continue
            elif current_state == 1:
                logger.debug(f"Article ID {article_id} already processed, skipping.")
                continue
            else:
                logger.error(f"Unsupported state {current_state} for article ID {article_id}")
                raise NotImplementedError(f"State {current_state} not supported")

        except Exception as e:
            logger.error(f"Unexpected error processing article ID {article_id}: {str(e)}")
            if current_state in [0, None]:
                try:
                    updated_article = Article(**article_data.copy())
                    updated_article.FlagExtractTopic = -1  # Mark as failed
                    persist.update_article_by_id(updated_article, article_id)
                    persist.refresh()
                except Exception as inner_e:
                    logger.error(f"Failed to update article ID {article_id}: {str(inner_e)}")
            else:
                persist.refresh()
            continue

    # Final refresh and cleanup
    persist.refresh()
    if bar:
        bar.close()
    logger.info("Topic extraction process completed.")