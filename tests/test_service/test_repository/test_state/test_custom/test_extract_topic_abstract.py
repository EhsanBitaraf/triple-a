import unittest
from unittest.mock import patch, Mock
from typing import Optional
import logging
from triplea.schemas.article import Article
from triplea.service.repository.state.custom.extract_topic import extract_topic_abstract

class TestExtractTopicAbstract(unittest.TestCase):
    def setUp(self):
        """Set up common mocks and test fixtures."""
        # Silence logging to avoid noise during tests
        logging.getLogger('').handlers = [logging.NullHandler()]
        
        # Mock the external extract_topic function
        self.patcher = patch('triplea.service.repository.state.custom.extract_topic.extract_topic')
        self.mock_extract_topic = self.patcher.start()
        
        # Create a sample Article object for testing
        self.sample_article = Article(
            Title="Sample Title",
            Abstract="Sample abstract text for testing."
        )

    def tearDown(self):
        """Clean up mocks after each test."""
        self.patcher.stop()

    def test_extract_topic_abstract_success(self):
        """Test successful topic extraction with valid inputs."""
        self.mock_extract_topic.return_value = ["topic1", "topic2", "topic3"]
        
        result = extract_topic_abstract(self.sample_article, method="textrank", top=5, threshold=0.1)
        
        self.assertIsInstance(result, Article)
        self.assertEqual(result.Topics, ["topic1", "topic2", "topic3"])
        self.assertEqual(result.FlagExtractTopic, 1)
        self.mock_extract_topic.assert_called_once_with(
            "Sample Title Sample abstract text for testing.",
            method="textrank",
            top=5,
            threshold=0.1
        )

    def test_extract_topic_abstract_none_article(self):
        """Test when article is None."""
        with self.assertRaisesRegex(ValueError, "Article object cannot be None."):
            extract_topic_abstract(None)

    def test_extract_topic_abstract_invalid_article_type(self):
        """Test when article is not an instance of Article."""
        invalid_article = {"Title": "Invalid", "Abstract": "Not an article"}
        with self.assertRaisesRegex(TypeError, "Input must be an instance of Article class."):
            extract_topic_abstract(invalid_article)

    def test_extract_topic_abstract_invalid_method_type(self):
        """Test when method is not a string."""
        with self.assertRaisesRegex(ValueError, "Method must be a string."):
            extract_topic_abstract(self.sample_article, method=123)

    def test_extract_topic_abstract_invalid_top_value(self):
        """Test when top is not a positive integer."""
        with self.assertRaisesRegex(ValueError, "Top must be a positive integer."):
            extract_topic_abstract(self.sample_article, top=0)
        
        with self.assertRaisesRegex(ValueError, "Top must be a positive integer."):
            extract_topic_abstract(self.sample_article, top=-5)

    def test_extract_topic_abstract_invalid_threshold(self):
        """Test when threshold is negative."""
        with self.assertRaisesRegex(ValueError, "Threshold must be a non-negative number."):
            extract_topic_abstract(self.sample_article, threshold=-0.1)

    def test_extract_topic_abstract_empty_text(self):
        """Test when title and abstract are empty."""
        empty_article = Article(Title=None, Abstract=None)
        result = extract_topic_abstract(empty_article)
        
        self.assertIsInstance(result, Article)
        self.assertEqual(result.FlagExtractTopic, -1)
        self.assertIsNone(result.Topics)
        self.mock_extract_topic.assert_not_called()

    def test_extract_topic_abstract_none_result(self):
        """Test when extract_topic returns None."""
        self.mock_extract_topic.return_value = None
        result = extract_topic_abstract(self.sample_article)
        
        self.assertIsInstance(result, Article)
        self.assertEqual(result.FlagExtractTopic, -1)
        self.assertIsNone(result.Topics)
        self.mock_extract_topic.assert_called_once()

    def test_extract_topic_abstract_value_error(self):
        """Test when extract_topic raises ValueError."""
        self.mock_extract_topic.side_effect = ValueError("Invalid extraction method")
        with self.assertRaisesRegex(ValueError, "Invalid extraction method"):
            extract_topic_abstract(self.sample_article)
        
        self.assertEqual(self.sample_article.FlagExtractTopic, -1)

    def test_extract_topic_abstract_unexpected_error(self):
        """Test when extract_topic raises an unexpected exception."""
        self.mock_extract_topic.side_effect = RuntimeError("Unexpected error")
        with self.assertRaisesRegex(RuntimeError, "Unexpected error"):
            extract_topic_abstract(self.sample_article)
        
        self.assertEqual(self.sample_article.FlagExtractTopic, -1)

    def test_extract_topic_abstract_edge_case_empty_strings(self):
        """Test when title and abstract are empty strings."""
        article = Article(Title="", Abstract="")
        result = extract_topic_abstract(article)
        
        self.assertIsInstance(result, Article)
        self.assertEqual(result.FlagExtractTopic, -1)
        self.assertIsNone(result.Topics)
        self.mock_extract_topic.assert_not_called()

    def test_extract_topic_abstract_edge_case_none_fields(self):
        """Test when title or abstract is None."""
        article = Article(Title=None, Abstract="Some text")
        self.mock_extract_topic.return_value = ["topic1"]
        
        result = extract_topic_abstract(article)
        
        self.assertIsInstance(result, Article)
        self.assertEqual(result.Topics, ["topic1"])
        self.assertEqual(result.FlagExtractTopic, 1)
        self.mock_extract_topic.assert_called_once_with(
            "Some text",
            method="textrank",
            top=10,
            threshold=0.0
        )

if __name__ == '__main__':
    unittest.main()