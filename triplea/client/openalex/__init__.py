from __future__ import annotations
import logging
from typing import Dict, Optional
from urllib.parse import quote_plus
import requests
from triplea.config.settings import SETTINGS
from ratelimit import limits, sleep_and_retry

# Configure logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# Define TPS (Transactions Per Second) limit for OpenAlex API (100 requests per second per IP)
OPENALEX_TPS_LIMIT = 9  # Conservative limit to avoid hitting rate limits
OPENALEX_BASE = "https://api.openalex.org"

@sleep_and_retry
@limits(calls=OPENALEX_TPS_LIMIT, period=1)
def openalex_by_doi(doi: str) -> Optional[Dict]:
    """Retrieve metadata for a work from the OpenAlex API using its DOI.

    This function sends a GET request to the OpenAlex API to fetch metadata for a
    scholarly work identified by its Digital Object Identifier (DOI). It supports
    proxy configuration and includes rate limiting to respect API constraints.

    Args:
        doi: The Digital Object Identifier (DOI) of the work (e.g., "10.1000/xyz123").

    Returns:
        Optional[Dict]: A dictionary containing the work's metadata if successful,
        or None if the work is not found (e.g., 404 status).

    Raises:
        ValueError: If the DOI is empty or None.
        requests.exceptions.Timeout: If the request times out.
        requests.exceptions.HTTPError: If the API returns an error status (e.g., 500).
        requests.exceptions.ConnectionError: If a network connection error occurs.
        requests.exceptions.RequestException: For other request-related errors.

    Examples:
        >>> result = openalex_by_doi("10.1000/xyz123")
        >>> if result:
        ...     print(result.get("title"))
        'Sample Article Title'

    Note:
        - The function uses a rate limiter to ensure compliance with OpenAlex API's
          TPS (Transactions Per Second) limit.
        - Proxy settings are applied if configured in SETTINGS.AAA_PROXY_HTTP or
          SETTINGS.AAA_PROXY_HTTPS.
        - The CLIENT_AGENT is used as the User-Agent header in the request.
        - Returns None only for non-critical errors like 404 (not found).
    """
    # Validate input
    if not doi:
        logger.error("DOI is empty or None")
        raise ValueError("DOI cannot be empty or None")

    # Prepare URL with encoded DOI
    encoded_doi = quote_plus(doi.strip())
    url = f"{OPENALEX_BASE}/works/https://doi.org/{encoded_doi}"
    logger.debug(f"Preparing request to OpenAlex API: {url}")

    # Configure proxies if available
    proxies = {}
    if hasattr(SETTINGS, 'AAA_PROXY_HTTP') and SETTINGS.AAA_PROXY_HTTP:
        proxies['http'] = SETTINGS.AAA_PROXY_HTTP
    if hasattr(SETTINGS, 'AAA_PROXY_HTTPS') and SETTINGS.AAA_PROXY_HTTPS:
        proxies['https'] = SETTINGS.AAA_PROXY_HTTPS

    # Set headers with user agent
    headers = {"User-Agent": SETTINGS.AAA_CLIENT_AGENT}

    try:
        # Send GET request with timeout and proxy settings
        logger.info(f"Sending request for DOI: {doi}")
        response = requests.get(url, headers=headers, proxies=proxies, timeout=20)
        response.raise_for_status()  # Raises an HTTPError for bad responses (e.g., 4xx, 5xx)

        # Check for successful response
        if response.status_code == 200:
            logger.info(f"Successfully retrieved metadata for DOI: {doi}")
            return response.json()
        else:
            logger.warning(f"Unexpected status code {response.status_code} for DOI: {doi}")
            return None

    except requests.exceptions.HTTPError as e:
        # Handle specific HTTP errors
        if e.response and e.response.status_code == 404:
            logger.warning(f"Work not found for DOI: {doi}")
            return None  # Maintain original behavior for 404
        logger.error(f"HTTP error occurred for DOI {doi}: {e}")
        raise  # Re-raise for other HTTP errors (e.g., 500)
    except requests.exceptions.Timeout as e:
        logger.error(f"Request timed out for DOI {doi}: {e}")
        raise  # Re-raise timeout errors
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error for DOI {doi}: {e}")
        raise  # Re-raise connection errors
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed for DOI {doi}: {e}")
        raise  # Re-raise other request-related errors
    except Exception as e:
        logger.exception(f"Unexpected error for DOI {doi}: {e}")
        raise  # Re-raise unexpected errors