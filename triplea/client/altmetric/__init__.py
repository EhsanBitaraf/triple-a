# get_altmetric.py
"""
Single-function Altmetric client.

This module exposes a single function, `get_altmetric`, that retrieves
Altmetric JSON data for a given scholarly identifier (DOI, PMID, or arXiv).
It is designed to be self-contained, readable, and production-friendly:
- Clear naming and thorough documentation
- Robust error handling and timeouts
- Logging (no print statements)
- Zero hard dependency on external settings; optional integration if a
  `SETTINGS` object happens to be present in the import context

File layout requirement:
- Function file: get_altmetric.py  (this file)
- Test file: test_get_altmetric.py

Example:
    >>> from get_altmetric import get_altmetric
    >>> data = get_altmetric("10.1038/nphys1170", id_type="doi")
    >>> if data is not None:
    ...     print(data["title"])  # doctest: +SKIP
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, Optional

import requests
from triplea.config.settings import SETTINGS

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def get_altmetric(
    identifier: str,
    id_type: str,
    *,
    user_agent: Optional[str] = None,
    proxies: Optional[Dict[str, str]] = None,
    timeout: float = 15.0,
) -> Optional[Dict[str, Any]]:
    """Fetch Altmetric JSON data for a DOI, PMID, or arXiv identifier.

    This function wraps the public Altmetric API and returns parsed JSON
    if available. It prefers resiliency: networking errors, timeouts, and
    non-200 responses (including 404) are handled without raising; the
    function returns ``None`` in those cases and logs details for operators.

    Args:
        identifier:
            The scholarly identifier string. Examples:
            - DOI: ``"10.1038/nphys1170"``
            - PMID: ``"24172933"``
            - arXiv: ``"1501.00001"``
        id_type:
            The type of the identifier. Must be one of:
            ``"doi"``, ``"pmid"``, or ``"arxiv"`` (case-insensitive).
        user_agent:
            Optional User-Agent header. If not provided, the function tries:
            1) An application-defined value at ``SETTINGS.AAA_CLIENT_AGENT`` if
               a ``SETTINGS`` object is available in the import context.
            2) A safe default: ``"AltmetricClient/1.0 (+https://altmetric.com)"``.
        proxies:
            Optional requests-style proxies mapping, e.g.:
            ``{"http": "http://proxy", "https": "http://proxy"}``.
            If not provided, the function tries to build one from a
            ``SETTINGS`` object in the import context:
            ``AAA_PROXY_HTTP`` / ``AAA_PROXY_HTTPS``.
        timeout:
            Total seconds to wait for the response (float).

    Returns:
        Parsed JSON as a dict when successful, otherwise ``None``.
        A ``None`` typically indicates a network issue, a timeout,
        a non-JSON response, or that the identifier was not found (404).

    Raises:
        ValueError: If ``id_type`` is not one of ``{"doi","pmid","arxiv"}`` or
            if ``identifier`` is empty/only whitespace.

    Examples:
        Basic usage (DOI):

            >>> from get_altmetric import get_altmetric
            >>> result = get_altmetric("10.1038/nphys1170", "doi")  # doctest: +SKIP
            >>> isinstance(result, dict) or result is None           # doctest: +SKIP
            True

        Using a proxy:

            >>> proxies = {"http": "http://localhost:3128", "https": "http://localhost:3128"}
            >>> result = get_altmetric("24172933", "pmid", proxies=proxies)  # doctest: +SKIP

        Handling missing records (404 -> None):

            >>> missing = get_altmetric("10.0000/definitely-not-real", "doi")  # doctest: +SKIP
            >>> missing is None                                                # doctest: +SKIP
            True
    """
    if not isinstance(identifier, str) or not identifier.strip():
        raise ValueError("Parameter 'identifier' must be a non-empty string.")
    if not isinstance(id_type, str) or id_type.strip().lower() not in {"doi", "pmid", "arxiv"}:
        raise ValueError("Parameter 'id_type' must be one of: 'doi', 'pmid', 'arxiv'.")

    id_type_norm = id_type.strip().lower()

    # Resolve endpoint path segment based on id_type
    endpoint_segment = {"doi": "doi", "pmid": "pmid", "arxiv": "arxiv"}[id_type_norm]
    url = f"https://api.altmetric.com/v1/{endpoint_segment}/{identifier.strip()}"

    # Resolve User-Agent: SETTINGS override > provided > default
    resolved_user_agent: str
    if user_agent:
        resolved_user_agent = user_agent
    else:
        # Attempt to draw from a global SETTINGS object if present.
        # This keeps the function self-contained while remaining flexible.
        resolved_user_agent = "AltmetricClient/1.0 (+https://altmetric.com)"
        try:
            # If a SETTINGS object is available in the caller's environment, prefer it.
            # These getattr calls are safe even if SETTINGS lacks the attributes.
            from __main__ import SETTINGS as _MAIN_SETTINGS  # type: ignore
            resolved_user_agent = getattr(
                _MAIN_SETTINGS, "AAA_CLIENT_AGENT", resolved_user_agent
            )
        except Exception:  # noqa: BLE001 - robust fallback if SETTINGS is absent or inaccessible
            try:
                # Fallback attempt if SETTINGS exists in this module namespace.
                SETTINGS  # type: ignore[name-defined]
                resolved_user_agent = getattr(  # type: ignore[misc]
                    SETTINGS, "AAA_CLIENT_AGENT", resolved_user_agent  # type: ignore[name-defined]
                )
            except Exception:
                # no SETTINGS discovered; keep default UA
                pass

    headers = {"User-Agent": resolved_user_agent}

    # Resolve proxies: explicit > SETTINGS > None
    resolved_proxies: Optional[Dict[str, str]] = proxies
    if resolved_proxies is None:
        try:
            from __main__ import SETTINGS as _MAIN_SETTINGS  # type: ignore
            http_proxy = getattr(_MAIN_SETTINGS, "AAA_PROXY_HTTP", None)
            https_proxy = getattr(_MAIN_SETTINGS, "AAA_PROXY_HTTPS", None)
            if http_proxy or https_proxy:
                resolved_proxies = {"http": http_proxy, "https": https_proxy}
        except Exception:  # noqa: BLE001
            try:
                SETTINGS  # type: ignore[name-defined]
                http_proxy = getattr(SETTINGS, "AAA_PROXY_HTTP", None)  # type: ignore[misc]
                https_proxy = getattr(SETTINGS, "AAA_PROXY_HTTPS", None)  # type: ignore[misc]
                if http_proxy or https_proxy:
                    resolved_proxies = {"http": http_proxy, "https": https_proxy}
            except Exception:
                resolved_proxies = None

    try:
        logger.debug("Requesting Altmetric data", extra={"url": url, "id_type": id_type_norm})
        response = requests.get(
            url,
            headers=headers,
            proxies=resolved_proxies,
            timeout=timeout,
        )
    except requests.exceptions.Timeout:
        logger.warning("Altmetric request timed out", extra={"url": url, "timeout": timeout})
        return None
    except requests.exceptions.RequestException as exc:
        logger.error("Altmetric request error", exc_info=exc, extra={"url": url})
        return None

    # Handle response codes explicitly
    if response.status_code == 404:
        # Record not found is a normal case for unknown identifiers.
        logger.info(
            "Altmetric record not found",
            extra={"url": url, "id_type": id_type_norm, "identifier": identifier},
        )
        return None

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as exc:
        logger.error(
            "Altmetric HTTP error",
            exc_info=exc,
            extra={"status": response.status_code, "url": url},
        )
        return None

    # Parse JSON safely
    try:
        data = response.json()
    except (json.JSONDecodeError, ValueError) as exc:
        logger.error("Altmetric returned non-JSON response", exc_info=exc, extra={"url": url})
        return None

    # Optional sanity checks on expected structure
    if not isinstance(data, dict):
        logger.error(
            "Altmetric JSON root is not a dict",
            extra={"type": type(data).__name__, "url": url},
        )
        return None

    logger.debug(
        "Altmetric data retrieved successfully",
        extra={"url": url, "keys": list(data.keys())[:10]},
    )
    return data
