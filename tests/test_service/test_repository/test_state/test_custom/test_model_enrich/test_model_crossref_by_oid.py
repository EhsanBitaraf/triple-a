"""
Test suite for model_crossref_by_oid function.
"""
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from triplea.schemas.article import Article
from triplea.service.repository.state.custom.model_enrich.__model_crossref_by_oid import model_crossref_by_oid


class TestModelCrossrefByOid(unittest.TestCase):
    """Test cases for model_crossref_by_oid function."""

    def setUp(self):
        """Set up common test fixtures and mocks."""
        # Create a basic valid article for testing
        self.valid_article = Article(
            DOI="10.1234/test.article",
            EnrichedData={}
        )
        
        # Mock Crossref response data
        self.mock_crossref_data = {
            "title": ["Test Article Title"],
            "author": [{"given": "John", "family": "Doe"}],
            "published": {"date-parts": [[2023, 1, 1]]}
        }
        
        # Patch the crossref_by_doi client
        self.crossref_patcher = patch(
            'triplea.service.repository.state.custom.model_enrich.__model_crossref_by_oid.crossref_by_doi'
        )
        self.mock_crossref_by_doi = self.crossref_patcher.start()
        
        # Patch logger to avoid noise during tests
        self.logger_patcher = patch(
            'triplea.service.repository.state.custom.model_enrich.__model_crossref_by_oid.logger'
        )
        self.mock_logger = self.logger_patcher.start()

    def tearDown(self):
        """Clean up after tests."""
        self.crossref_patcher.stop()
        self.logger_patcher.stop()

    def test_invalid_input_type(self):
        """Test that function raises ValueError for non-Article input."""
        with self.assertRaises(ValueError) as context:
            model_crossref_by_oid("not_an_article")
        
        self.assertIn("must be an instance of Article", str(context.exception))
        self.mock_logger.error.assert_called_once()

    def test_article_without_doi(self):
        """Test function returns None when article has no DOI."""
        article = Article(DOI=None, EnrichedData={})
        
        result = model_crossref_by_oid(article)
        
        self.assertIsNone(result)
        self.mock_logger.debug.assert_called_with("Article has no DOI, skipping Crossref enrichment")

    def test_empty_string_doi(self):
        """Test function processes empty string DOI (treats it as valid)."""
        # Empty string DOI is NOT None, so function will proceed
        self.mock_crossref_by_doi.return_value = self.mock_crossref_data
        article = Article(DOI="", EnrichedData={})
        
        result = model_crossref_by_oid(article)
        
        # Function should process empty string DOI and return article with enriched data
        self.assertIsNotNone(result)
        self.assertIn('crossref', result.EnrichedData)
        self.mock_crossref_by_doi.assert_called_with("")

    def test_successful_first_time_enrichment(self):
        """Test successful Crossref enrichment for first time."""
        self.mock_crossref_by_doi.return_value = self.mock_crossref_data
        
        result = model_crossref_by_oid(self.valid_article)
        
        self.assertIsNotNone(result)
        self.assertIn('crossref', result.EnrichedData)
        self.assertIn('data', result.EnrichedData['crossref'])
        self.assertIn('date', result.EnrichedData['crossref'])
        self.assertEqual(result.EnrichedData['crossref']['data'], self.mock_crossref_data)
        self.mock_logger.info.assert_called_with(f"Adding Crossref data for DOI: {self.valid_article.DOI}")

    def test_crossref_returns_none(self):
        """Test function returns None when Crossref returns no data."""
        self.mock_crossref_by_doi.return_value = None
        
        result = model_crossref_by_oid(self.valid_article)
        
        self.assertIsNone(result)
        self.mock_logger.warning.assert_called_with(f"No Crossref data found for DOI: {self.valid_article.DOI}")

    def test_existing_crossref_data_no_overwrite(self):
        """Test function returns None when Crossref data exists and overwrite=False."""
        # The function calls Crossref API first, then checks for existing data
        self.mock_crossref_by_doi.return_value = self.mock_crossref_data
        
        article = Article(
            DOI="10.1234/test.article",
            EnrichedData={'crossref': {'date': datetime.now(), 'data': {'existing': 'data'}}}
        )
        
        result = model_crossref_by_oid(article, overwrite=False)
        
        # Should return None because data exists and overwrite=False
        self.assertIsNone(result)
        self.mock_logger.debug.assert_called_with(f"crossref data already exists for DOI: {article.DOI}, skipping")
        # Crossref client SHOULD be called (function calls it before checking existing data)
        self.mock_crossref_by_doi.assert_called_with(article.DOI)

    def test_existing_crossref_data_with_overwrite(self):
        """Test function overwrites existing Crossref data when overwrite=True."""
        self.mock_crossref_by_doi.return_value = self.mock_crossref_data
        
        article = Article(
            DOI="10.1234/test.article",
            EnrichedData={'crossref': {'date': datetime(2020, 1, 1), 'data': {'old': 'data'}}}
        )
        
        result = model_crossref_by_oid(article, overwrite=True)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.EnrichedData['crossref']['data'], self.mock_crossref_data)
        self.mock_logger.info.assert_called_with(f"Overwriting existing Crossref data for DOI: {article.DOI}")

    def test_initializes_none_enriched_data(self):
        """Test function initializes EnrichedData when it's None."""
        self.mock_crossref_by_doi.return_value = self.mock_crossref_data
        article = Article(DOI="10.1234/test.article", EnrichedData=None)
        
        result = model_crossref_by_oid(article)
        
        self.assertIsNotNone(result)
        self.assertIsInstance(result.EnrichedData, dict)
        self.assertIn('crossref', result.EnrichedData)

    def test_crossref_client_exception(self):
        """Test function re-raises exceptions from Crossref client."""
        self.mock_crossref_by_doi.side_effect = Exception("Crossref API error")
        
        with self.assertRaises(Exception) as context:
            model_crossref_by_oid(self.valid_article)
        
        self.assertIn("Crossref API error", str(context.exception))
        self.mock_logger.error.assert_called_once()

    def test_enriched_data_structure(self):
        """Test that enriched data has correct structure with date and data."""
        self.mock_crossref_by_doi.return_value = self.mock_crossref_data
        
        result = model_crossref_by_oid(self.valid_article)
        
        self.assertIsNotNone(result)
        crossref_data = result.EnrichedData['crossref']
        self.assertIn('date', crossref_data)
        self.assertIn('data', crossref_data)
        self.assertIsInstance(crossref_data['date'], datetime)
        self.assertEqual(crossref_data['data'], self.mock_crossref_data)

    def test_crossref_api_called_with_correct_doi(self):
        """Test that Crossref API is called with the correct DOI."""
        self.mock_crossref_by_doi.return_value = self.mock_crossref_data
        test_doi = "10.1000/test-doi"
        article = Article(DOI=test_doi, EnrichedData={})
        
        model_crossref_by_oid(article)
        
        self.mock_crossref_by_doi.assert_called_once_with(test_doi)


if __name__ == '__main__':
    unittest.main()