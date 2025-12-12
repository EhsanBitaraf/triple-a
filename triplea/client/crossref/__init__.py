"""
CrossRef API client for retrieving publication metadata by DOI.

This module provides functionality to query the CrossRef API to fetch
bibliographic metadata for publications using their Digital Object Identifier (DOI).
"""

import logging
import time
from typing import Dict
from urllib.parse import quote_plus

import requests
from triplea.config.settings import SETTINGS

# Module configuration
CROSSREF_BASE = "https://api.crossref.org"
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class RateLimiter:
    """
    Simple rate limiter to control API request frequency.
    
    This class implements a basic TPS (Transactions Per Second) limiter
    using a sliding window approach.
    
    Attributes:
        tps (float): Maximum transactions per second allowed.
        min_interval (float): Minimum time interval between requests in seconds.
        last_request_time (float): Timestamp of the last request.
    """
    
    def __init__(self, tps: float = 2.0):
        """
        Initialize the rate limiter.
        
        Args:
            tps: Transactions per second limit. Default is 2.0 TPS.
        
        Examples:
            >>> limiter = RateLimiter(tps=1.5)
            >>> limiter.wait()  # Waits if necessary before allowing next request
        """
        self.tps = tps
        self.min_interval = 1.0 / tps
        self.last_request_time = 0.0
        logger.debug(f"RateLimiter initialized with TPS: {tps}")
    
    def wait(self) -> None:
        """
        Wait if necessary to maintain the configured TPS rate.
        
        This method calculates the time elapsed since the last request
        and sleeps for the remaining time if needed to maintain the TPS limit.
        """
        current_time = time.time()
        elapsed = current_time - self.last_request_time
        
        if elapsed < self.min_interval:
            sleep_time = self.min_interval - elapsed
            logger.debug(f"Rate limiting: sleeping for {sleep_time:.3f} seconds")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()


# Global rate limiter instance (2 TPS as per CrossRef recommended limits)
_rate_limiter = RateLimiter(tps=2.0)


def crossref_by_doi(
    doi: str,
    use_rate_limiter: bool = True,
    timeout: int = 20
) -> Dict:
    """
    Retrieve publication metadata from CrossRef API using a DOI.
    
    This function queries the CrossRef REST API to fetch bibliographic metadata
    for a publication identified by its DOI. It implements proper error handling,
    rate limiting, proxy support, and custom user agent configuration.
    
    Args:
        doi: Digital Object Identifier for the publication. Must be a non-empty string.
        use_rate_limiter: Whether to apply rate limiting (default: True).
            Set to False for testing or when handling rate limiting externally.
        timeout: Request timeout in seconds (default: 20).
    
    Returns:
        A dictionary containing the publication metadata.
        The returned dictionary follows the CrossRef API schema with fields like:
        - 'title': Publication title
        - 'author': List of authors
        - 'published-print': Publication date
        - 'DOI': The DOI identifier
        And many other bibliographic fields.
    
    Raises:
        ValueError: If DOI is None or empty string, or if response data is invalid.
        TimeoutError: If the request times out.
        ConnectionError: If connection to CrossRef API fails.
        RuntimeError: For HTTP errors (404, 429, 5xx) or other API-related errors.
        requests.exceptions.RequestException: For other request-related errors.
    
    Examples:
        >>> # Basic usage
        >>> try:
        ...     metadata = crossref_by_doi("10.1234/example.doi")
        ...     print(metadata.get('title'))
        ... except RuntimeError as e:
        ...     print(f"API error: {e}")
        ... except (TimeoutError, ConnectionError) as e:
        ...     print(f"Network error: {e}")
        ['Example Publication Title']
        
        >>> # Invalid DOI
        >>> try:
        ...     result = crossref_by_doi("")
        ... except ValueError as e:
        ...     print(f"Invalid input: {e}")
        Invalid input: DOI cannot be None or empty
        
        >>> # DOI not found
        >>> try:
        ...     result = crossref_by_doi("10.9999/invalid")
        ... except RuntimeError as e:
        ...     print(f"Not found: {e}")
        Not found: DOI not found in CrossRef (404): 10.9999/invalid
    
    Note:
        - The function respects CrossRef's rate limiting guidelines (2 TPS by default)
        - Proxy settings are configured via SETTINGS.AAA_PROXY_HTTP
        - User agent is set via SETTINGS.AAA_CLIENT_AGENT
        - CrossRef API documentation: https://api.crossref.org
    """
    # Input validation
    if not doi:
        logger.error("DOI validation failed: DOI is None or empty")
        raise ValueError("DOI cannot be None or empty")
    
    # Strip whitespace from DOI
    doi = doi.strip()
    logger.info(f"Fetching CrossRef metadata for DOI: {doi}")
    
    # Apply rate limiting
    if use_rate_limiter:
        _rate_limiter.wait()
    
    # Construct API URL with URL-encoded DOI
    url = f"{CROSSREF_BASE}/works/{quote_plus(doi)}"
    logger.debug(f"CrossRef API URL: {url}")
    
    # Configure proxies if provided
    proxies = {}
    if SETTINGS.AAA_PROXY_HTTP:
        proxies = {
            'http': SETTINGS.AAA_PROXY_HTTP,
            'https': SETTINGS.AAA_PROXY_HTTP
        }
        logger.debug(f"Using proxy: {SETTINGS.AAA_PROXY_HTTP}")
    else:
        logger.debug("No proxy configured")
    
    # Configure headers with custom user agent
    headers = {
        'User-Agent': SETTINGS.AAA_CLIENT_AGENT
    }
    logger.debug(f"Using User-Agent: {SETTINGS.AAA_CLIENT_AGENT}")
    
    # Make API request
    try:
        resp = requests.get(
            url,
            headers=headers,
            proxies=proxies if proxies else None,
            timeout=timeout
        )
        
        logger.debug(f"Response status code: {resp.status_code}")
        
        # Check for successful response
        if resp.status_code == 200:
            try:
                data = resp.json()
                message = data.get('message')
                
                if message:
                    logger.info(f"Successfully retrieved metadata for DOI: {doi}")
                    return message
                else:
                    error_msg = f"No 'message' field in response for DOI: {doi}"
                    logger.error(error_msg)
                    raise ValueError(error_msg)
                    
            except (ValueError, KeyError) as json_err:
                error_msg = f"Invalid JSON response for DOI {doi}: {json_err}"
                logger.error(error_msg)
                raise ValueError(error_msg) from json_err
        
        elif resp.status_code == 404:
            error_msg = f"DOI not found in CrossRef (404): {doi}"
            logger.warning(error_msg)
            raise RuntimeError(error_msg)
        
        elif resp.status_code == 429:
            error_msg = f"Rate limit exceeded (429) for DOI: {doi}. Consider reducing TPS."
            logger.error(error_msg)
            raise RuntimeError(error_msg)
        
        else:
            error_msg = (
                f"HTTP error {resp.status_code} for DOI: {doi}. "
                f"Response: {resp.text[:200]}"
            )
            logger.warning(error_msg)
            raise RuntimeError(error_msg)
    
    except requests.exceptions.Timeout as timeout_err:
        error_msg = f"Request timeout for DOI {doi} after {timeout}s: {timeout_err}"
        logger.error(error_msg)
        raise TimeoutError(error_msg) from timeout_err
    
    except requests.exceptions.ConnectionError as conn_err:
        error_msg = f"Connection error for DOI {doi}: {conn_err}"
        logger.error(error_msg)
        raise ConnectionError(error_msg) from conn_err
    
    except requests.exceptions.RequestException as req_err:
        error_msg = f"Request exception for DOI {doi}: {req_err}"
        logger.error(error_msg)
        raise RuntimeError(error_msg) from req_err
    
    except (ValueError, TimeoutError, ConnectionError, RuntimeError):
        # Re-raise our exceptions
        raise
    
    except Exception as e:
        error_msg = f"Unexpected error fetching DOI {doi}: {type(e).__name__}: {e}"
        logger.error(error_msg)
        raise RuntimeError(error_msg) from e