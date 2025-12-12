# tests/test_client/test_crossref_by_doi.py
import unittest
from unittest.mock import patch, MagicMock, Mock
import requests

from triplea.client.crossref import crossref_by_doi


def make_response(status=200, payload=None, text="", json_side_effect=None):
    """Create a mocked requests.Response-like object."""
    resp = Mock()
    resp.status_code = status
    resp.text = text
    if json_side_effect is not None:
        resp.json.side_effect = json_side_effect
    else:
        resp.json.return_value = payload if payload is not None else {}
    return resp


class TestCrossrefByDoi(unittest.TestCase):
    """Tests for the `crossref_by_doi` function."""

    def setUp(self):
        """Common patches: silence logger, stub settings, rate limiter, and requests.get."""
        # Silence logger to keep test output clean
        self.logger_patcher = patch("triplea.client.crossref.logger")
        self.mock_logger = self.logger_patcher.start()
        self.addCleanup(self.logger_patcher.stop)

        # Stub SETTINGS object used by the module
        self.settings_patcher = patch("triplea.client.crossref.SETTINGS")
        self.mock_settings = self.settings_patcher.start()
        self.addCleanup(self.settings_patcher.stop)
        self.mock_settings.AAA_PROXY_HTTP = None
        self.mock_settings.AAA_CLIENT_AGENT = "testsuite/1.0 (+https://example.test)"

        # Avoid real rate-limiting sleeps
        self.limiter_patcher = patch("triplea.client.crossref._rate_limiter")
        self.mock_rate_limiter = self.limiter_patcher.start()
        self.addCleanup(self.limiter_patcher.stop)
        self.mock_rate_limiter.wait = MagicMock()

        # Patch requests.get; each test will control return/side_effects
        self.requests_get_patcher = patch("triplea.client.crossref.requests.get")
        self.mock_get = self.requests_get_patcher.start()
        self.addCleanup(self.requests_get_patcher.stop)

    # -------------------- Success paths --------------------

    def test_returns_message_on_status_200(self):
        """Should return the `message` dict when API responds with 200 and valid JSON."""
        doi = "10.1000/xyz"
        payload = {"message": {"DOI": doi, "title": ["Hello"]}}
        self.mock_get.return_value = make_response(status=200, payload=payload)

        result = crossref_by_doi(doi)

        self.assertEqual(result, payload["message"])
        self.mock_rate_limiter.wait.assert_called_once()
        self.mock_get.assert_called_once()
        _, kwargs = self.mock_get.call_args
        # Headers and default timeout
        self.assertIn("headers", kwargs)
        self.assertEqual(kwargs["headers"]["User-Agent"], "testsuite/1.0 (+https://example.test)")
        self.assertEqual(kwargs["timeout"], 20)
        # No proxies when not configured
        self.assertIsNone(kwargs.get("proxies"))

    def test_trims_whitespace_and_urlencodes_doi(self):
        """Should trim whitespace and URL-encode spaces and slashes within DOI."""
        raw = " 10.1000/a b "
        payload = {"message": {"DOI": "10.1000/a b", "title": ["T"]}}
        self.mock_get.return_value = make_response(status=200, payload=payload)

        crossref_by_doi(raw)

        # requests.get could be called with positional or keyword URL argument
        if self.mock_get.call_args[0]:
            url = self.mock_get.call_args[0][0]
        else:
            url = self.mock_get.call_args[1]["url"]
        # Slash is encoded as %2F and space as '+'
        self.assertIn("/works/10.1000%2Fa+b", url)

    def test_respects_custom_timeout(self):
        """Should pass the provided timeout to requests.get."""
        doi = "10.1000/t"
        self.mock_get.return_value = make_response(
            status=200, payload={"message": {"DOI": doi, "title": ["T"]}}
        )

        crossref_by_doi(doi, timeout=3)

        _, kwargs = self.mock_get.call_args
        self.assertEqual(kwargs["timeout"], 3)

    def test_skips_rate_limiter_when_disabled(self):
        """Should not invoke rate limiter when use_rate_limiter=False."""
        doi = "10.1000/norl"
        self.mock_get.return_value = make_response(
            status=200, payload={"message": {"DOI": doi, "title": ["T"]}}
        )

        crossref_by_doi(doi, use_rate_limiter=False)

        self.mock_rate_limiter.wait.assert_not_called()

    def test_uses_proxy_when_configured(self):
        """Should pass both http and https proxies when SETTINGS.AAA_PROXY_HTTP is set."""
        self.mock_settings.AAA_PROXY_HTTP = "http://proxy.local:8080"
        doi = "10.1000/proxy"
        self.mock_get.return_value = make_response(
            status=200, payload={"message": {"DOI": doi, "title": ["T"]}}
        )

        crossref_by_doi(doi)

        _, kwargs = self.mock_get.call_args
        self.assertEqual(
            kwargs["proxies"],
            {"http": "http://proxy.local:8080", "https": "http://proxy.local:8080"},
        )

    # -------------------- Input validation --------------------

    def test_empty_or_none_doi_raises_value_error(self):
        """Should raise ValueError when DOI is empty or None."""
        with self.assertRaisesRegex(ValueError, "DOI cannot be None or empty"):
            crossref_by_doi("")
        with self.assertRaisesRegex(ValueError, "DOI cannot be None or empty"):
            crossref_by_doi(None)  # type: ignore[arg-type]

    # -------------------- API error handling --------------------

    def test_200_without_message_field_raises_value_error(self):
        """200 OK without 'message' should raise ValueError with helpful text."""
        self.mock_get.return_value = make_response(status=200, payload={"status": "ok"})

        with self.assertRaisesRegex(ValueError, "No 'message' field in response"):
            crossref_by_doi("10.1000/nomsg")

    def test_invalid_json_value_error_is_wrapped_as_value_error(self):
        """If response.json() raises ValueError, function should raise ValueError with context."""
        self.mock_get.return_value = make_response(
            status=200, json_side_effect=ValueError("bad json")
        )

        with self.assertRaisesRegex(ValueError, r"Invalid JSON response for DOI 10\.1000/bad"):
            crossref_by_doi("10.1000/bad")

    def test_invalid_json_other_exception_is_wrapped_as_runtime_error(self):
        """If response.json() raises unexpected TypeError, it should become RuntimeError (outer catch-all)."""
        self.mock_get.return_value = make_response(
            status=200, json_side_effect=TypeError("weird")
        )

        with self.assertRaisesRegex(RuntimeError, r"Unexpected error fetching DOI 10\.1000/weird:"):
            crossref_by_doi("10.1000/weird")

    def test_404_raises_runtime_error(self):
        """404 from API should raise a RuntimeError with DOI included."""
        self.mock_get.return_value = make_response(status=404, text="Not Found")

        with self.assertRaisesRegex(RuntimeError, r"DOI not found in CrossRef \(404\): 10\.9999/missing"):
            crossref_by_doi("10.9999/missing")

    def test_429_rate_limited_raises_runtime_error(self):
        """429 from API should raise a RuntimeError indicating rate limit exceeded."""
        self.mock_get.return_value = make_response(status=429, text="Too Many Requests")

        with self.assertRaisesRegex(RuntimeError, r"Rate limit exceeded \(429\) for DOI: 10\.1000/slow"):
            crossref_by_doi("10.1000/slow")

    def test_5xx_raises_runtime_error_with_snippet(self):
        """Any non-200/404/429 HTTP status should raise RuntimeError and include status code."""
        long_text = "X" * 500
        self.mock_get.return_value = make_response(status=503, text=long_text)

        with self.assertRaisesRegex(RuntimeError, r"HTTP error 503 for DOI: 10\.1000/down\. Response:"):
            crossref_by_doi("10.1000/down")

    # -------------------- Requests exceptions mapping --------------------

    def test_requests_timeout_maps_to_timeout_error(self):
        """requests.exceptions.Timeout should map to built-in TimeoutError with message."""
        self.mock_get.side_effect = requests.exceptions.Timeout("boom")

        with self.assertRaisesRegex(TimeoutError, r"Request timeout for DOI 10\.1000/t after 20s:"):
            crossref_by_doi("10.1000/t")

    def test_requests_connection_error_maps_to_connection_error(self):
        """requests.exceptions.ConnectionError should map to built-in ConnectionError with message."""
        self.mock_get.side_effect = requests.exceptions.ConnectionError("no route")

        with self.assertRaisesRegex(ConnectionError, r"Connection error for DOI 10\.1000/c:"):
            crossref_by_doi("10.1000/c")

    def test_requests_generic_exception_maps_to_runtime_error(self):
        """Generic requests.exceptions.RequestException should map to RuntimeError."""
        self.mock_get.side_effect = requests.exceptions.RequestException("oops")

        with self.assertRaisesRegex(RuntimeError, r"Request exception for DOI 10\.1000/x:"):
            crossref_by_doi("10.1000/x")


if __name__ == "__main__":
    unittest.main(verbosity=2)
