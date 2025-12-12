


# test_get_altmetric.py
"""
Basic unit tests for get_altmetric.

Naming:
- Test file name: test_get_altmetric.py

These tests mock network calls to avoid real HTTP requests and cover:
- Successful 200 JSON response
- 404 -> None behavior
- HTTP error (e.g., 500) -> None
- Timeout -> None
- Validation errors for bad inputs
"""

from __future__ import annotations

import json
from typing import Any, Dict
from unittest import mock

import pytest
import requests

from triplea.client.altmetric import get_altmetric

class _Resp:
    """Lightweight mockable response object."""

    def __init__(self, status_code: int, payload: Dict[str, Any] | None = None) -> None:
        self.status_code = status_code
        self._payload = payload

    def raise_for_status(self) -> None:
        if 400 <= self.status_code:
            raise requests.exceptions.HTTPError(f"HTTP {self.status_code}")

    def json(self) -> Dict[str, Any]:
        if self._payload is None:
            raise json.JSONDecodeError("nope", "doc", 0)
        return self._payload


def test_successful_doi_returns_dict() -> None:
    payload = {"title": "Example title", "score": 42}
    with mock.patch("requests.get", return_value=_Resp(200, payload)):
        result = get_altmetric("10.1038/nphys1170", "doi")
    assert isinstance(result, dict)
    assert result["score"] == 42


def test_404_returns_none() -> None:
    with mock.patch("requests.get", return_value=_Resp(404, {})):
        result = get_altmetric("10.0000/not-real", "doi")
    assert result is None


def test_http_error_returns_none() -> None:
    with mock.patch("requests.get", return_value=_Resp(500, {"error": "server"})):
        result = get_altmetric("24172933", "pmid")
    assert result is None


def test_timeout_returns_none() -> None:
    with mock.patch("requests.get", side_effect=requests.exceptions.Timeout()):
        result = get_altmetric("1501.00001", "arxiv", timeout=0.001)
    assert result is None


@pytest.mark.parametrize("bad_id", ["", "   ", 123, None])
def test_invalid_identifier_raises_value_error(bad_id: Any) -> None:
    with pytest.raises(ValueError):
        get_altmetric(bad_id, "doi")  # type: ignore[arg-type]


# @pytest.mark.parametrize("bad_type", ["", "   ", "DOI ", "pm d", "isbn", 5, None])
# def test_invalid_id_type_raises_value_error(bad_type: Any) -> None:
#     with pytest.raises(ValueError):
#         get_altmetric("10.1038/nphys1170", bad_type)  # type: ignore[arg-type]
