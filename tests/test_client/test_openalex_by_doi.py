import unittest
from unittest.mock import patch, Mock
import logging
from triplea.client.openalex import openalex_by_doi
from triplea.config.settings import SETTINGS
import requests

class TestOpenalexByDoi(unittest.TestCase):
    def setUp(self):
        """Set up common mocks and configurations for tests."""
        # Silence logging during tests
        logging.getLogger('').handlers = [logging.NullHandler()]
        
        # Mock SETTINGS attributes
        self.settings_patcher = patch('triplea.client.openalex.SETTINGS')
        self.mock_settings = self.settings_patcher.start()
        self.mock_settings.AAA_CLIENT_AGENT = "TestClient/1.0"
        self.mock_settings.AAA_PROXY_HTTP = None
        self.mock_settings.AAA_PROXY_HTTPS = None
        
        # Mock requests.get
        self.requests_patcher = patch('triplea.client.openalex.requests.get')
        self.mock_requests_get = self.requests_patcher.start()
        
        # Mock ratelimit.limits to bypass rate limiting entirely
        self.ratelimit_patcher = patch('triplea.client.openalex.ratelimit.limits')
        self.mock_ratelimit = self.ratelimit_patcher.start()
        # Return the original function without any rate-limiting logic
        self.mock_ratelimit.side_effect = lambda calls, period, raise_on_limit=True: lambda func: func

    def tearDown(self):
        """Clean up patches after each test."""
        self.settings_patcher.stop()
        self.requests_patcher.stop()
        self.ratelimit_patcher.stop()

    def test_valid_doi_successful_response(self):
        """Test successful API response for a valid DOI."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"title": "Test Article", "id": "W123"}
        self.mock_requests_get.return_value = mock_response

        result = openalex_by_doi("10.1000/xyz123")
        
        self.assertIsNotNone(result)
        self.assertEqual(result["title"], "Test Article")
        self.mock_requests_get.assert_called_once_with(
            "https://api.openalex.org/works/https://doi.org/10.1000%2Fxyz123",
            headers={"User-Agent": "TestClient/1.0"},
            proxies={},
            timeout=20
        )

    def test_empty_doi_raises_value_error(self):
        """Test that empty DOI raises ValueError with correct message."""
        with self.assertRaisesRegex(ValueError, "DOI cannot be empty or None"):
            openalex_by_doi("")

        with self.assertRaisesRegex(ValueError, "DOI cannot be empty or None"):
            openalex_by_doi(None)

    def test_doi_with_whitespace(self):
        """Test DOI with leading/trailing whitespace is handled correctly."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"title": "Test Article"}
        self.mock_requests_get.return_value = mock_response

        result = openalex_by_doi("  10.1000/xyz123  ")
        
        self.assertIsNotNone(result)
        self.assertEqual(result["title"], "Test Article")
        self.mock_requests_get.assert_called_once_with(
            "https://api.openalex.org/works/https://doi.org/10.1000%2Fxyz123",
            headers={"User-Agent": "TestClient/1.0"},
            proxies={},
            timeout=20
        )

    def test_404_not_found_returns_none(self):
        """Test 404 response returns None."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        self.mock_requests_get.return_value = mock_response

        result = openalex_by_doi("10.1000/nonexistent")
        
        self.assertIsNone(result)
        self.mock_requests_get.assert_called_once()

    def test_http_error_500_raises_exception(self):
        """Test 500 HTTP error raises HTTPError."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        self.mock_requests_get.return_value = mock_response

        with self.assertRaises(requests.exceptions.HTTPError):
            openalex_by_doi("10.1000/xyz123")

    def test_timeout_raises_timeout_exception(self):
        """Test request timeout raises Timeout exception."""
        self.mock_requests_get.side_effect = requests.exceptions.Timeout("Request timed out")

        with self.assertRaises(requests.exceptions.Timeout):
            openalex_by_doi("10.1000/xyz123")

    def test_connection_error_raises_connection_exception(self):
        """Test connection error raises ConnectionError."""
        self.mock_requests_get.side_effect = requests.exceptions.ConnectionError("Connection failed")

        with self.assertRaises(requests.exceptions.ConnectionError):
            openalex_by_doi("10.1000/xyz123")

    def test_generic_request_exception(self):
        """Test generic request exception is raised."""
        self.mock_requests_get.side_effect = requests.exceptions.RequestException("Generic request error")

        with self.assertRaises(requests.exceptions.RequestException):
            openalex_by_doi("10.1000/xyz123")

    def test_proxy_settings_applied(self):
        """Test proxy settings are applied when configured."""
        self.mock_settings.AAA_PROXY_HTTP = "http://proxy:8080"
        self.mock_settings.AAA_PROXY_HTTPS = "https://proxy:8080"
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"title": "Test Article"}
        self.mock_requests_get.return_value = mock_response

        result = openalex_by_doi("10.1000/xyz123")
        
        self.assertIsNotNone(result)
        self.mock_requests_get.assert_called_once_with(
            "https://api.openalex.org/works/https://doi.org/10.1000%2Fxyz123",
            headers={"User-Agent": "TestClient/1.0"},
            proxies={"http": "http://proxy:8080", "https": "https://proxy:8080"},
            timeout=20
        )

    # def test_unexpected_status_code_raises_http_error(self):
    #     """Test unexpected status code (not 200 or 404) raises HTTPError."""
    #     mock_response = Mock()
    #     mock_response.status_code = 429  # Too Many Requests
    #     mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
    #     self.mock_requests_get.return_value = mock_response

    #     with self.assertRaises(requests.exceptions.HTTPError):
    #         openalex_by_doi("10.1000/xyz123")

    # def test_unexpected_exception(self):
    #     """Test unexpected exception is logged and re-raised."""
    #     self.mock_requests_get.side_effect = Exception("Unexpected error")

    #     with self.assertRaises(Exception, msg="Unexpected error"):
    #         openalex_by_doi("10.1000/xyz123")

if __name__ == '__main__':
    unittest.main()