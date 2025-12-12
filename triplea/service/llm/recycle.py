import triplea.service.repository.persist as PERSIST
import click
from triplea.schemas.article import Article
from triplea.utils.general import print_error
from triplea.service.click_logger import logger
import warnings
from triplea.utils.general import get_tqdm

def reset_flag_llm_by_fx(fx, limit_sample=0, proccess_bar=True):
    """
    Reset "FlagShortReviewByLLM" flag for articles based on a user-defined condition.

    ```
    This function retrieves all articles whose `FlagShortReviewByLLM` custom state (cstate)
    is currently set to `1`, then applies a user-provided function `fx(article)` to each
    article object. If the function returns `True`, the flag is reset to `0` for that article.

    Parameters
    ----------
    fx : callable
        A function that takes an `Article` object as input and returns a boolean.
        If it returns `True`, the article’s "FlagShortReviewByLLM" field will be reset to `0`.

    limit_sample : int, optional, default=0
        Limits how many articles to process.  
        - If `0`, all matching articles are processed (unlimited).  
        - If greater than `0`, stops after processing the specified number of articles.

    proccess_bar : bool, optional, default=True
        If `True`, displays a progress bar using `click.progressbar` during processing.

    Behavior
    --------
    - Retrieves a list of article IDs with `cstate=1` for "FlagShortReviewByLLM".
    - Iterates through each article:
        1. Loads article data from persistence layer.
        2. Constructs an `Article` object.
        3. Applies `fx(article)` to decide whether to reset the flag.
        4. Updates the database if necessary.
    - Displays a progress bar showing the number of updated articles (if enabled).
    - Handles exceptions gracefully and logs errors per article.
    - Calls `PERSIST.refresh()` at the end to sync the persistence layer.

    Returns
    -------
    None
        This function performs in-place updates via the `PERSIST` layer and returns nothing.

    Notes
    -----
    - This function assumes the existence of a `PERSIST` object with methods:
        - `get_article_id_list_by_cstate(cstate_value, field_name)`
        - `get_article_by_id(article_id)`
        - `update_cstate_by_id(article_id, field_name, new_value)`
        - `refresh()`
    - Also assumes an `Article` class capable of being initialized with keyword arguments from a dict.
    - Designed to help batch-reset articles previously flagged by an LLM for review.

    Example
    -------
    >>> def is_valid_for_reset(article):
    ...     return "approved" in article.tags
    >>> reset_flag_llm_by_fx(is_valid_for_reset, limit_sample=100, proccess_bar=True)
    >>> # Resets the flag for up to 100 articles tagged as "approved"
    """

    l_id = PERSIST.get_article_id_list_by_cstate(1, "FlagShortReviewByLLM")
    n = 0
    change_number = 0
    doc_number = len(l_id)
    if doc_number == 0:
        return
    if proccess_bar:
        # bar = click.progressbar(length=doc_number, show_pos=True, show_percent=True)
        tqdm = get_tqdm()
        bar = tqdm(total=len(l_id), desc="Processing ")

    for id in l_id:
        n = n + 1
        try:
            a = PERSIST.get_article_by_id(id)
            article = Article(**a.copy())
            if fx(article) is True:
                # Change FlagShortReviewByLLM to 1
                PERSIST.update_cstate_by_id(id, "FlagShortReviewByLLM", 0)
                change_number = change_number + 1

            if proccess_bar:
                # bar.label = f"""{change_number} Article(s) Updated."""
                bar.set_description(f"{change_number} Article(s) Updated.")
                bar.update(1)

            if limit_sample != 0:  # Unlimited
                if n > limit_sample:
                    break
        except Exception:
            print()
            print(logger.ERROR(f"article. ID = {id}"))
            print_error()
    PERSIST.refresh()



def reset_flag_llm_by_function(TemplateID, fx, limit_sample=0, proccess_bar=True):
    warnings.warn(
        """reset_flag_llm_by_function() is deprecated
          and will be removed in a future version.
          You can use reset_flag_llm_by_fx()""",
        DeprecationWarning,
        stacklevel=2
    )
    l_id = PERSIST.get_article_id_list_by_cstate(1, "FlagShortReviewByLLM")
    n = 0
    change_number = 0
    doc_number = len(l_id)
    if doc_number == 0:
        return
    if proccess_bar:
        bar = click.progressbar(length=doc_number, show_pos=True, show_percent=True)

    for id in l_id:
        n = n + 1
        try:
            a = PERSIST.get_article_by_id(id)
            article = Article(**a.copy())
            if fx(TemplateID, article.ReviewLLM) is True:
                # Change FlagShortReviewByLLM to 1
                PERSIST.update_cstate_by_id(id, "FlagShortReviewByLLM", 0)
                change_number = change_number + 1

            if proccess_bar:
                bar.label = f"""{change_number} Article(s) Updated."""
                bar.update(1)

            if limit_sample != 0:  # Unlimited
                if n > limit_sample:
                    break
        except Exception:
            print()
            print(logger.ERROR(f"article. ID = {id}"))
            print_error()
    PERSIST.refresh()
