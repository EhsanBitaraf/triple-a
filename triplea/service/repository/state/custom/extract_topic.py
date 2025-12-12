import logging
from typing import Optional
from triplea.client.topic_extraction import extract_topic
from triplea.schemas.article import Article

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def extract_topic_abstract(
    article: Article,
    method: str = "textrank",
    top: int = 10,
    threshold: float = 0.0
) -> Optional[Article]:
    """Extracts topics from an article's title and abstract using a specified method.

    This function processes the article's title and abstract to extract key topics
    using the `extract_topic` function. It updates the article's `Topics` field with
    the extracted topics and sets the `FlagExtractTopic` to indicate success (1) or
    failure (-1). The combined text of title and abstract is cleaned by removing
    newlines before topic extraction.

    Args:
        article: An Article object containing title and abstract.
        method: The topic extraction method to use (default: "textrank").
        top: The maximum number of topics to extract (default: 10).
        threshold: The minimum score threshold for extracted topics (default: 0.0).

    Returns:
        Optional[Article]: The updated Article object with extracted topics, or None
            if the input is invalid or topic extraction fails critically.

    Raises:
        ValueError: If the article is None or if method, top, or threshold have
            invalid values.
        TypeError: If the article is not an instance of the Article class.

    Examples:
        >>> from triplea.schemas.article import Article
        >>> article = Article(Title="Sample Title", Abstract="Sample abstract text.")
        >>> updated_article = extract_topic_abstract(article, method="textrank", top=5)
        >>> print(updated_article.Topics)
        ["topic1", "topic2", ...]

    """
    # Validate input parameters
    if article is None:
        logger.error("Article object is None.")
        raise ValueError("Article object cannot be None.")

    if not isinstance(article, Article):
        logger.error(f"Expected Article object, got {type(article).__name__}.")
        raise TypeError("Input must be an instance of Article class.")

    if not isinstance(method, str):
        logger.error(f"Invalid method type: {type(method).__name__}, expected string.")
        raise ValueError("Method must be a string.")

    if not isinstance(top, int) or top <= 0:
        logger.error(f"Invalid top value: {top}, must be a positive integer.")
        raise ValueError("Top must be a positive integer.")

    if not isinstance(threshold, (int, float)) or threshold < 0:
        logger.error(f"Invalid threshold value: {threshold}, must be non-negative.")
        raise ValueError("Threshold must be a non-negative number.")

    # Set the flag to indicate topic extraction is in progress
    article.FlagExtractTopic = 1

    # Safely handle title and abstract, defaulting to empty strings if None
    title = article.Title if article.Title is not None else ""
    abstract = article.Abstract if article.Abstract is not None else ""

    # Combine and clean text
    text = f"{title} {abstract}".replace("\n", " ").strip()
    if not text:
        logger.warning("Combined title and abstract is empty; no topics extracted.")
        article.FlagExtractTopic = -1
        return article

    # Perform topic extraction
    try:
        result = extract_topic(text, method=method, top=top, threshold=threshold)
        if result is None:
            logger.warning(f"Topic extraction returned None for method '{method}'.")
            article.FlagExtractTopic = -1
            return article

        article.Topics = result
        logger.info(f"Successfully extracted {len(result)} topics for article.")
    except ValueError as ve:
        logger.error(f"ValueError during topic extraction: {str(ve)}")
        article.FlagExtractTopic = -1
        raise
    except Exception as e:
        logger.error(f"Unexpected error during topic extraction: {str(e)}")
        article.FlagExtractTopic = -1
        raise

    return article