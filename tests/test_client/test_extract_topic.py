import unittest
from unittest.mock import patch, Mock
import json
import logging
import requests
from triplea.client.topic_extraction import extract_topic
from triplea.config.settings import SETTINGS

class TestExtractTopic(unittest.TestCase):
    def setUp(self):
        """Set up common mocks and test fixtures."""
        # Silence logging to avoid noise during tests
        logging.getLogger('').handlers = [logging.NullHandler()]
        
        # Mock requests.Session.post
        self.session_patcher = patch('triplea.client.topic_extraction.session')
        self.mock_session = self.session_patcher.start()
        self.mock_post = self.mock_session.post
        
        # Mock SETTINGS attributes
        self.settings_patcher = patch('triplea.client.topic_extraction.SETTINGS')
        self.mock_settings = self.settings_patcher.start()
        self.mock_settings.AAA_TOPIC_EXTRACT_ENDPOINT = "https://api.example.com/topics"
        self.mock_settings.AAA_CLIENT_AGENT = "TestAgent/1.0"
        self.mock_settings.AAA_PROXY_HTTP = None
        self.mock_settings.AAA_PROXY_HTTPS = None

    def tearDown(self):
        """Clean up patchers."""
        self.session_patcher.stop()
        self.settings_patcher.stop()

    def test_extract_topic_success(self):
        """Test successful topic extraction with valid input."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success", "r": ["topic1", "topic2"]}
        self.mock_post.return_value = mock_response
        
        text = "This is a sample text about AI."
        method = "LDA"
        top = 5
        threshold = 0.1

        # Act
        result = extract_topic(text, method, top, threshold)

        # Assert
        self.mock_post.assert_called_once_with(
            url="https://api.example.com/topics/",
            data=json.dumps({
                "Text": "This is a sample text about AI.",
                "Method": "LDA",
                "Top": 5,
                "Threshold": 0.1
            }),
            headers={"User-Agent": "TestAgent/1.0", "Content-Type": "application/json"},
            proxies=None,
            timeout=10
        )
        self.assertEqual(result, ["topic1", "topic2"])

    def test_extract_topic_empty_text(self):
        """Test ValueError for empty text input."""
        with self.assertRaisesRegex(ValueError, "Text cannot be empty or whitespace."):
            extract_topic("", "LDA")
        
        with self.assertRaisesRegex(ValueError, "Text cannot be empty or whitespace."):
            extract_topic("   ", "LDA")

    def test_extract_topic_invalid_method(self):
        """Test ValueError for invalid method input."""
        with self.assertRaisesRegex(ValueError, "Method must be a non-empty string."):
            extract_topic("Sample text", "")
        
        with self.assertRaisesRegex(ValueError, "Method must be a non-empty string."):
            extract_topic("Sample text", None)

    def test_extract_topic_timeout(self):
        """Test handling of request timeout."""
        self.mock_post.side_effect = requests.exceptions.Timeout("Request timed out")
        with self.assertRaisesRegex(requests.exceptions.Timeout, "API request timed out."):
            extract_topic("Sample text", "LDA")

    def test_extract_topic_connection_error(self):
        """Test handling of connection error."""
        self.mock_post.side_effect = requests.exceptions.ConnectionError("Connection failed")
        with self.assertRaisesRegex(requests.exceptions.ConnectionError, "Failed to connect to the API."):
            extract_topic("Sample text", "LDA")

    def test_extract_topic_http_error_404(self):
        """Test handling of 404 HTTP error (returns empty list)."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        self.mock_post.return_value = mock_response
        
        result = extract_topic("Sample text", "LDA")
        self.assertEqual(result, [])

    def test_extract_topic_http_error_500(self):
        """Test handling of non-404 HTTP error."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error")
        self.mock_post.return_value = mock_response
        
        with self.assertRaisesRegex(requests.exceptions.HTTPError, "HTTP error 500 occurred."):
            extract_topic("Sample text", "LDA")

    def test_extract_topic_invalid_json(self):
        """Test handling of invalid JSON response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "{}", 0)
        self.mock_post.return_value = mock_response
        
        with self.assertRaisesRegex(json.JSONDecodeError, "Invalid JSON response from API."):
            extract_topic("Sample text", "LDA")

    def test_extract_topic_missing_response_keys(self):
        """Test handling of missing 'status' or 'r' keys in response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"wrong_key": "value"}
        self.mock_post.return_value = mock_response
        
        with self.assertRaisesRegex(KeyError, "Invalid response format: 'status' or 'r' key missing."):
            extract_topic("Sample text", "LDA")

    def test_extract_topic_with_proxy(self):
        """Test API call with proxy settings."""
        # Update mock settings for proxies
        self.mock_settings.AAA_PROXY_HTTP = "http://proxy.example.com"
        self.mock_settings.AAA_PROXY_HTTPS = "https://proxy.example.com"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success", "r": ["topic1"]}
        self.mock_post.return_value = mock_response
        
        extract_topic("Sample text", "LDA")
        
        self.mock_post.assert_called_once_with(
            url="https://api.example.com/topics/",
            data=json.dumps({
                "Text": "Sample text",
                "Method": "LDA",
                "Top": 10,
                "Threshold": 0
            }),
            headers={"User-Agent": "TestAgent/1.0", "Content-Type": "application/json"},
            proxies={"http": "http://proxy.example.com", "https": "https://proxy.example.com"},
            timeout=10
        )

    def test_extract_topic_edge_case_empty_response(self):
        """Test handling of empty topic list in response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success", "r": []}
        self.mock_post.return_value = mock_response
        
        result = extract_topic("Sample text", "LDA")
        self.assertEqual(result, [])

    def test_extract_topic_edge_case_large_top(self):
        """Test handling of large 'top' parameter."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success", "r": ["topic1"]}
        self.mock_post.return_value = mock_response
        
        result = extract_topic("Sample text", "LDA", top=1000)
        self.assertEqual(result, ["topic1"])

if __name__ == '__main__':
    unittest.main()