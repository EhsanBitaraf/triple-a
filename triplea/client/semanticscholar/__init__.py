
from __future__ import annotations

import logging
from typing import Dict, Iterable, Optional, Union
from urllib.parse import quote

import requests
from ratelimit import limits, sleep_and_retry
from triplea.config.settings import SETTINGS

# -----------------------------------------------------------------------------
# Logging configuration (library-friendly)
# -----------------------------------------------------------------------------
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
SEMANTIC_SCHOLAR_TPS_LIMIT = 2  # Conservative limit to avoid rate-limit errors
SEMANTIC_SCHOLAR_BASE = "https://api.semanticscholar.org/graph/v1"
API_KEY = ""  # Optionally set your Semantic Scholar API key here
TIMEOUT_DEFAULT = 20

# NOTE: Field names follow the Semantic Scholar Graph API schema.
DEFAULT_FIELDS = [
    "paperId",
    "title",
    "abstract",
    "year",
    "publicationDate",
    "venue",
    "authors.authorId",
    "authors.name",
    "externalIds",
    "citationCount",
    "referenceCount",
    "influentialCitationCount",
    "s2FieldsOfStudy",
    "openAccessPdf",
]


@sleep_and_retry
@limits(calls=SEMANTIC_SCHOLAR_TPS_LIMIT, period=1)
def semanticscholar_by_doi(
    doi: str,
    fields: Optional[Union[str, Iterable[str]]] = DEFAULT_FIELDS,
    timeout: Union[int, float] = TIMEOUT_DEFAULT,
) -> Optional[Dict]:
    """Fetch paper metadata from Semantic Scholar by DOI.

    This function queries the **Semantic Scholar Graph API** for a paper record
    identified by the given DOI and returns the parsed JSON response. It applies
    a conservative rate limit and uses robust error handling that:
      * Raises specific exceptions for invalid inputs or server/network problems.
      * Returns ``None`` only for the non-critical case of HTTP 404 (not found).

    Args:
        doi (str): Digital Object Identifier (e.g., "10.1038/nphys1170").
        fields (Optional[Union[str, Iterable[str]]], optional):
            Fields to request from the API. Can be a comma-separated string or
            an iterable of field names. If ``None``, all default fields from the
            API are returned (which may be large). Defaults to ``DEFAULT_FIELDS``.
        timeout (Union[int, float], optional):
            Request timeout in seconds. Must be a positive number.
            Defaults to ``TIMEOUT_DEFAULT`` (20 seconds).

    Returns:
        Optional[Dict]: Parsed JSON for the paper if found; ``None`` if the paper
        does not exist (HTTP 404).

    Raises:
        ValueError: If `doi` is empty/invalid, `timeout` is non-positive,
            or `fields` has an invalid type/content.
        requests.exceptions.Timeout: If the request times out.
        requests.exceptions.HTTPError: For non-404 HTTP errors (4xx/5xx).
        requests.exceptions.RequestException: For other network-related errors.

    Examples:
        >>> data = semanticscholar_by_doi("10.1038/nphys1170")
        >>> isinstance(data, dict)
        True
    """
    # -------------------------------------------------------------------------
    # Input validation
    # -------------------------------------------------------------------------
    if not isinstance(doi, str) or not doi.strip():
        logger.error("Invalid DOI: DOI must be a non-empty string.")
        raise ValueError("DOI must be a non-empty string.")

    if not isinstance(timeout, (int, float)) or timeout <= 0:
        logger.error("Invalid timeout: must be a positive number. Given: %r", timeout)
        raise ValueError("Timeout must be a positive number (seconds).")

    params: Dict[str, str] = {}
    if fields is not None:
        if isinstance(fields, str):
            csv = ",".join([f.strip() for f in fields.split(",") if f.strip()])
            if not csv:
                logger.error("Invalid fields: provided string is empty after stripping.")
                raise ValueError("Fields string must contain at least one field.")
            params["fields"] = csv
        elif isinstance(fields, Iterable):
            try:
                field_list = [str(f).strip() for f in fields if str(f).strip()]
            except Exception as exc:
                logger.exception("Failed to normalize 'fields' iterable.")
                raise ValueError("Fields must be an iterable of non-empty strings.") from exc
            if not field_list:
                logger.error("Invalid fields: iterable is empty after normalization.")
                raise ValueError("Fields iterable must contain at least one non-empty string.")
            params["fields"] = ",".join(field_list)
        else:
            logger.error("Invalid fields type: %r", type(fields))
            raise ValueError("Fields must be a string, an iterable of strings, or None.")

    # -------------------------------------------------------------------------
    # Build request
    # -------------------------------------------------------------------------
    identifier = f"DOI:{doi.strip()}"
    url = f"{SEMANTIC_SCHOLAR_BASE}/paper/{quote(identifier, safe=':')}"

    headers = {
        "Accept": "application/json",
        "User-Agent": SETTINGS.AAA_CLIENT_AGENT,  # Always set User-Agent
    }
    if API_KEY:
        headers["x-api-key"] = API_KEY

    # -------------------------------------------------------------------------
    # Configure proxies (only if provided)
    # -------------------------------------------------------------------------
    proxies = {}
    if getattr(SETTINGS, "AAA_PROXY_HTTP", None):
        proxies["http"] = SETTINGS.AAA_PROXY_HTTP
    if getattr(SETTINGS, "AAA_PROXY_HTTPS", None):
        proxies["https"] = SETTINGS.AAA_PROXY_HTTPS

    # -------------------------------------------------------------------------
    # Execute request with robust error handling
    # -------------------------------------------------------------------------
    try:
        logger.debug(
            "Requesting Semantic Scholar API: %s | params=%s | proxies=%s",
            url,
            params or "{}",
            "configured" if proxies else "none",
        )
        response = requests.get(url, params=params, headers=headers, timeout=timeout, proxies=proxies or None)
    except requests.exceptions.Timeout as exc:
        logger.error("Semantic Scholar request timed out for DOI '%s'.", doi)
        raise
    except requests.exceptions.RequestException as exc:
        logger.exception("Network error while requesting Semantic Scholar for DOI '%s'.", doi)
        raise

    if response.status_code != 200:
        try:
            error_detail = response.json()
        except Exception:
            error_detail = response.text

        if response.status_code == 404:
            logger.warning(
                "Paper not found on Semantic Scholar (HTTP 404) for DOI '%s'. Detail: %s",
                doi,
                error_detail,
            )
            return None

        message = (
            f"Semantic Scholar API error (HTTP {response.status_code}) for DOI "
            f"'{doi}'. Detail: {error_detail}"
        )
        logger.error(message)
        raise requests.exceptions.HTTPError(message, response=response)

    try:
        data = response.json()
    except ValueError as exc:
        logger.exception("Failed to decode JSON from Semantic Scholar for DOI '%s'.", doi)
        raise requests.exceptions.RequestException(
            "Invalid JSON received from Semantic Scholar."
        ) from exc

    logger.debug("Semantic Scholar response successfully received for DOI '%s'.", doi)
    return data





# from __future__ import annotations
# import logging
# from typing import Dict, Optional
# from urllib.parse import quote_plus
# import requests
# import time
# from triplea.config.settings import SETTINGS
# from ratelimit import limits, sleep_and_retry
# from urllib.parse import quote

# # Configure logging
# logger = logging.getLogger(__name__)
# logger.addHandler(logging.NullHandler())


# SEMANTICSCHOLAR_TPS_LIMIT = 2  # Conservative limit to avoid hitting rate limits
# SEMANTICSCHOLAR_BASE = "https://api.openalex.org"
# API_KEY = ""
# TIMEOUT = 20
# DEFUALT_FIELDS = [
#     "paperId",
#     "title",
#     "abstract",
#     "year",
#     "publicationDate",
#     "venue",
#     "authors.authorId",
#     "authors.name",
#     "externalIds",
#     "citationCount",
#     "referenceCount",
#     "influentialCitationCount",
#     "s2FieldsOfStudy",
#     "openAccessPdf",
# ]


# @sleep_and_retry
# @limits(calls=SEMANTICSCHOLAR_TPS_LIMIT, period=1)
# def semanticscholar_by_doi(doi: str,
#                            fields = DEFUALT_FIELDS,
#                             timeout = TIMEOUT ) -> Optional[Dict]:



#     pid = quote(doi, safe=":")  
#     url = f"{SEMANTICSCHOLAR_BASE}/paper/{pid}"

#     params = {}
#     if fields:
#         if isinstance(fields, (list, tuple, set)):
#             params["fields"] = ",".join(fields)
#         elif isinstance(fields, str):
#             params["fields"] = fields 
#         else:
#             raise ValueError("error")

#     headers = {"Accept": "application/json"}
#     if API_KEY:
#         headers["x-api-key"] = API_KEY

#     resp = requests.get(url, params=params, headers=headers, timeout=timeout)
#     if resp.status_code != 200:
#         try:
#             detail = resp.json()
#         except Exception:
#             detail = resp.text
#             raise 


#     return resp.json()


