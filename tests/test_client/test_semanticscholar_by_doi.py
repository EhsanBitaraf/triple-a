# tests/path/to/test_semanticscholar_by_doi.py
"""
Unit tests for `semanticscholar_by_doi`.

These tests:
- Use unittest + unittest.mock for all external dependencies.
- Are self-contained (no network/database).
- Include positive, negative, and edge cases.
- Assert specific exceptions and messages.
- Silence logging noise.
- Are runnable with both pytest and unittest.
"""

import logging
import unittest
from unittest.mock import Mock, patch
from urllib.parse import quote

import requests

# Import the function under test
from triplea.client.semanticscholar import semanticscholar_by_doi


class TestSemanticscholarByDoi(unittest.TestCase):
    """Tests for the `semanticscholar_by_doi` function."""

    def setUp(self):
        """Set up common patches and defaults for each test."""
        # Silence loggers to avoid noisy output during tests
        logging.disable(logging.CRITICAL)

        # Patch requests.get at the module path where it is used
        self.p_get = patch("triplea.client.semanticscholar.requests.get")
        self.mock_get = self.p_get.start()

        # Patch SETTINGS object used inside the module
        self.p_settings = patch("triplea.client.semanticscholar.SETTINGS")
        self.mock_settings = self.p_settings.start()

        # Provide default SETTINGS values used by the function
        self.mock_settings.AAA_CLIENT_AGENT = "test-agent"
        # Proxies default to not configured unless a test sets them
        self.mock_settings.AAA_PROXY_HTTP = None
        self.mock_settings.AAA_PROXY_HTTPS = None

    def tearDown(self):
        """Tear down patches and re-enable logging."""
        self.p_get.stop()
        self.p_settings.stop()
        logging.disable(logging.NOTSET)

    # ---------------------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------------------
    @staticmethod
    def _make_response(status_code=200, json_data=None, text="<html/>"):
        """Create a mock Response-like object with desired behavior."""
        resp = Mock()
        resp.status_code = status_code
        if json_data is not None:
            resp.json = Mock(return_value=json_data)
        else:
            # If not provided, raise ValueError to simulate invalid JSON
            def _raise():
                raise ValueError("No JSON")

            resp.json = Mock(side_effect=_raise)
        resp.text = text
        return resp

    # # ---------------------------------------------------------------------
    # # Positive path
    # # ---------------------------------------------------------------------
    # def test_successful_response_returns_dict_and_correct_request(self):
    #     """It should return parsed JSON on 200 and construct request correctly."""
    #     doi = "10.1038/nphys1170"
    #     expected_json = {"paperId": "abc123", "title": "Quantum magic"}
    #     self.mock_get.return_value = self._make_response(200, expected_json)

    #     result = semanticscholar_by_doi(doi)

    #     self.assertIsInstance(result, dict)
    #     self.assertEqual(result, expected_json)

    #     # Verify correct URL construction with quoted DOI prefix "DOI:"
    #     base = "https://api.semanticscholar.org/graph/v1"
    #     identifier = f"DOI:{doi}"
    #     expected_url = f"{base}/paper/{quote(identifier, safe=':')}"
    #     self.mock_get.assert_called_once()
    #     called_url = self.mock_get.call_args.kwargs["url"]
    #     self.assertEqual(called_url, expected_url)

    #     # Verify headers include required User-Agent from SETTINGS
    #     headers = self.mock_get.call_args.kwargs["headers"]
    #     self.assertEqual(headers.get("User-Agent"), "test-agent")
    #     self.assertEqual(headers.get("Accept"), "application/json")

    #     # Proxies should be None when not configured
    #     self.assertIsNone(self.mock_get.call_args.kwargs["proxies"])

    # ---------------------------------------------------------------------
    # 404 -> None
    # ---------------------------------------------------------------------
    def test_404_returns_none_without_raising(self):
        """HTTP 404 should return None (paper not found)."""
        doi = "10.9999/does-not-exist"
        self.mock_get.return_value = self._make_response(404, {"error": "Not found"})
        self.assertIsNone(semanticscholar_by_doi(doi))

    # ---------------------------------------------------------------------
    # HTTP errors (non-404)
    # ---------------------------------------------------------------------
    def test_http_500_raises_http_error_with_message(self):
        """Non-404 HTTP errors should raise HTTPError with informative message."""
        doi = "10.1000/server-error"
        self.mock_get.return_value = self._make_response(500, {"error": "Server down"})

        with self.assertRaises(requests.exceptions.HTTPError) as cm:
            semanticscholar_by_doi(doi)
        msg = str(cm.exception)
        self.assertIn("HTTP 500", msg)
        self.assertIn(doi, msg)
        # The exception should have a response attached
        self.assertIsNotNone(cm.exception.response)

    # ---------------------------------------------------------------------
    # Network-level exceptions
    # ---------------------------------------------------------------------
    def test_timeout_raises_timeout(self):
        """Timeouts from requests.get should propagate as requests.exceptions.Timeout."""
        self.mock_get.side_effect = requests.exceptions.Timeout("Timed out")
        with self.assertRaises(requests.exceptions.Timeout):
            semanticscholar_by_doi("10.1000/timeout", timeout=0.1)

    def test_request_exception_is_propagated(self):
        """Other RequestException should propagate."""
        self.mock_get.side_effect = requests.exceptions.RequestException("Network down")
        with self.assertRaises(requests.exceptions.RequestException):
            semanticscholar_by_doi("10.1000/network")

    # ---------------------------------------------------------------------
    # Invalid inputs
    # ---------------------------------------------------------------------
    def test_invalid_doi_raises_value_error(self):
        """Empty DOI should raise ValueError with a clear message."""
        with self.assertRaises(ValueError) as cm:
            semanticscholar_by_doi("")
        self.assertIn("DOI must be a non-empty string", str(cm.exception))

    def test_invalid_timeout_raises_value_error(self):
        """Non-positive timeout should raise ValueError."""
        with self.assertRaises(ValueError) as cm:
            semanticscholar_by_doi("10.1000/ok", timeout=0)
        self.assertIn("Timeout must be a positive number", str(cm.exception))

    def test_fields_wrong_type_raises_value_error(self):
        """Fields of an unsupported type should raise ValueError."""
        with self.assertRaises(ValueError) as cm:
            semanticscholar_by_doi("10.1000/ok", fields=123)  # type: ignore[arg-type]
        self.assertIn("Fields must be a string, an iterable of strings, or None", str(cm.exception))

    def test_fields_empty_string_after_strip_raises(self):
        """Fields='' should raise ValueError after normalization."""
        with self.assertRaises(ValueError) as cm:
            semanticscholar_by_doi("10.1000/ok", fields=" , ,  ")
        self.assertIn("Fields string must contain at least one field", str(cm.exception))

    def test_fields_iterable_empty_after_normalization_raises(self):
        """An iterable with only empty/whitespace fields should raise ValueError."""
        with self.assertRaises(ValueError) as cm:
            semanticscholar_by_doi("10.1000/ok", fields=["  ", "", "   "])
        self.assertIn("Fields iterable must contain at least one non-empty string", str(cm.exception))

    # ---------------------------------------------------------------------
    # Fields normalization
    # ---------------------------------------------------------------------
    def test_fields_string_normalization_is_used_in_params(self):
        """Comma-separated string should be normalized and sent as 'fields' param."""
        self.mock_get.return_value = self._make_response(200, {"ok": True})
        semanticscholar_by_doi("10.1000/ok", fields=" title , authors.name ,,  year ")

        params = self.mock_get.call_args.kwargs["params"]
        self.assertEqual(params.get("fields"), "title,authors.name,year")

    def test_fields_iterable_normalization_is_used_in_params(self):
        """Iterable should be normalized and sent as 'fields' param."""
        self.mock_get.return_value = self._make_response(200, {"ok": True})
        semanticscholar_by_doi("10.1000/ok", fields=[" title ", " ", "year", "citationCount"])

        params = self.mock_get.call_args.kwargs["params"]
        self.assertEqual(params.get("fields"), "title,year,citationCount")

    # ---------------------------------------------------------------------
    # Response decoding
    # ---------------------------------------------------------------------
    def test_invalid_json_in_200_response_raises_request_exception(self):
        """If JSON decoding fails on a 200, raise RequestException with clear message."""
        # A 200 response whose .json() raises ValueError
        resp = self._make_response(200, json_data=None, text="not-json")
        self.mock_get.return_value = resp

        with self.assertRaises(requests.exceptions.RequestException) as cm:
            semanticscholar_by_doi("10.1000/bad-json")
        self.assertIn("Invalid JSON received from Semantic Scholar", str(cm.exception))

    # ---------------------------------------------------------------------
    # Proxies configuration
    # ---------------------------------------------------------------------
    def test_proxies_are_passed_when_configured(self):
        """If proxy settings are present, they should be sent to requests.get."""
        self.mock_settings.AAA_PROXY_HTTP = "http://proxy.local:8080"
        self.mock_settings.AAA_PROXY_HTTPS = "https://secure-proxy.local:8443"
        self.mock_get.return_value = self._make_response(200, {"ok": True})

        semanticscholar_by_doi("10.1000/with-proxy")

        proxies = self.mock_get.call_args.kwargs["proxies"]
        self.assertEqual(
            proxies,
            {
                "http": "http://proxy.local:8080",
                "https": "https://secure-proxy.local:8443",
            },
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
