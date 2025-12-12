"""Unit tests for model_semanticscholar_by_doi.

These tests patch external dependencies and avoid any network/database access.
They cover positive, negative, and edge cases, use clear naming, and adhere to
PEP8. They are executable with both pytest and unittest.
"""

import logging
import types
import unittest
from datetime import datetime, timedelta
from importlib import import_module
from unittest.mock import MagicMock, patch


MODULE_PATH = (
    "triplea.service.repository.state.custom.model_enrich.__model_semanticscholar_by_doi"
)


class DummyArticle:
    """Minimal stand-in for triplea.schemas.article.Article used in tests."""

    def __init__(self, doi=None, enriched=None):
        self.DOI = doi
        self.EnrichedData = enriched


class TestModelSemanticScholarByDoi(unittest.TestCase):
    """Tests for model_semanticscholar_by_doi behavior."""

    def setUp(self):
        """Prepare common patches and a clean module reference each test."""
        # Import target module
        self.mod = import_module(MODULE_PATH)

        # Patch the module's Article symbol so isinstance checks work locally.
        self.original_article_symbol = getattr(self.mod, "Article", None)
        setattr(self.mod, "Article", DummyArticle)

        # Silence noisy loggers by patching the module-level logger with a mock.
        self.logger_patcher = patch(f"{MODULE_PATH}.logger", autospec=True)
        self.mock_logger = self.logger_patcher.start()

        # Patch the external client call used by the function
        self.client_patcher = patch(
            f"{MODULE_PATH}.semanticscholar_by_doi", autospec=True
        )
        self.mock_client = self.client_patcher.start()

        # Shortcuts to the function under test
        self.func = getattr(self.mod, "model_semanticscholar_by_doi")

    def tearDown(self):
        """Stop patches and restore module state."""
        self.client_patcher.stop()
        self.logger_patcher.stop()
        # Restore original Article symbol if it existed
        if self.original_article_symbol is not None:
            setattr(self.mod, "Article", self.original_article_symbol)

    # ----------------------
    # Negative / error cases
    # ----------------------

    def test_invalid_article_type_raises_value_error(self):
        """Passing a non-Article instance should raise ValueError with message."""
        with self.assertRaises(ValueError) as ctx:
            self.func(article={"DOI": "10.1234/xyz"}, overwrite=False)

        self.assertIn("must be an instance of Article", str(ctx.exception))
        self.mock_logger.error.assert_called()  # error should be logged

    def test_no_doi_returns_none_and_logs_debug(self):
        """When DOI is missing, function should return None and not call client."""
        article = DummyArticle(doi=None, enriched={})
        result = self.func(article, overwrite=False)

        self.assertIsNone(result)
        self.mock_client.assert_not_called()
        self.mock_logger.debug.assert_called()  # debug log for skipping

    def test_client_returns_none_results_in_none_and_warning(self):
        """If external client returns None, function returns None and warns."""
        article = DummyArticle(doi="10.1000/abc", enriched={})
        self.mock_client.return_value = None

        result = self.func(article, overwrite=False)

        self.assertIsNone(result)
        self.mock_client.assert_called_once_with("10.1000/abc")
        self.mock_logger.warning.assert_called()  # warning about no data

    def test_client_error_is_propagated_and_logged(self):
        """Exceptions from client should be logged and re-raised."""
        article = DummyArticle(doi="10.1000/boom", enriched={})
        self.mock_client.side_effect = RuntimeError("kaboom")

        with self.assertRaises(RuntimeError) as ctx:
            self.func(article, overwrite=True)

        self.assertIn("kaboom", str(ctx.exception))
        # Ensure it attempted a fetch and logged an error
        self.mock_client.assert_called_once_with("10.1000/boom")
        self.mock_logger.error.assert_called()

    # ----------------------
    # Positive / main flows
    # ----------------------

    def test_adds_semanticscholar_data_first_time(self):
        """First-time enrichment adds data and returns the article."""
        article = DummyArticle(doi="10.1000/new", enriched={})
        payload = {"title": "Sample", "year": 2024}
        self.mock_client.return_value = payload

        result = self.func(article, overwrite=False)

        self.assertIs(result, article)
        self.mock_client.assert_called_once_with("10.1000/new")

        self.assertIn("semanticscholar", article.EnrichedData)
        entry = article.EnrichedData["semanticscholar"]
        self.assertIsInstance(entry, dict)
        self.assertIn("date", entry)
        self.assertIn("data", entry)
        self.assertEqual(entry["data"], payload)
        self.assertIsInstance(entry["date"], datetime)
        # sanity: the recorded date should be very recent (within 5 seconds)
        self.assertLess(datetime.now() - entry["date"], timedelta(seconds=5))
        self.mock_logger.info.assert_called()  # info about adding

    def test_skips_when_existing_and_overwrite_false(self):
        """Existing data and overwrite=False should skip and not call client."""
        existing = {
            "semanticscholar": {
                "date": datetime(2020, 1, 1),
                "data": {"title": "Old"},
            }
        }
        article = DummyArticle(doi="10.1000/existing", enriched=existing)

        result = self.func(article, overwrite=False)

        self.assertIsNone(result)
        self.mock_client.assert_not_called()
        self.mock_logger.debug.assert_called()  # debug about skipping

    def test_overwrites_when_existing_and_overwrite_true(self):
        """Existing data and overwrite=True should fetch, overwrite, and return."""
        existing = {
            "semanticscholar": {
                "date": datetime(2020, 1, 1),
                "data": {"title": "Old"},
            }
        }
        article = DummyArticle(doi="10.1000/existing", enriched=existing)
        new_payload = {"title": "New", "citations": 42}
        self.mock_client.return_value = new_payload

        result = self.func(article, overwrite=True)

        self.assertIs(result, article)
        self.mock_client.assert_called_once_with("10.1000/existing")

        entry = article.EnrichedData["semanticscholar"]
        self.assertEqual(entry["data"], new_payload)
        self.assertIsInstance(entry["date"], datetime)
        self.mock_logger.info.assert_called()  # info about overwriting

    def test_initializes_enricheddata_when_none(self):
        """If EnrichedData is None and overwrite=True, it initializes and adds data."""
        article = DummyArticle(doi="10.1000/init", enriched=None)
        payload = {"ok": True}
        self.mock_client.return_value = payload

        result = self.func(article, overwrite=True)

        self.assertIs(result, article)
        self.assertIsInstance(article.EnrichedData, dict)
        self.assertIn("semanticscholar", article.EnrichedData)
        self.assertEqual(article.EnrichedData["semanticscholar"]["data"], payload)


    def test_overwrite_true_without_existing_still_adds(self):
        """With overwrite=True and no existing key, it should behave like add."""
        article = DummyArticle(doi="10.1000/add", enriched={})
        payload = {"k": "v"}
        self.mock_client.return_value = payload

        result = self.func(article, overwrite=True)

        self.assertIs(result, article)
        self.mock_client.assert_called_once_with("10.1000/add")
        self.assertEqual(
            article.EnrichedData["semanticscholar"]["data"], payload
        )
        # Either info or debug can be logged depending on branch; ensure some call
        self.assertTrue(
            self.mock_logger.info.called or self.mock_logger.debug.called
        )


if __name__ == "__main__":
    # Allow running via `python -m unittest -v tests.unit.test_model_semanticscholar_by_doi`
    # and compatible with `pytest -v`.
    # logging.getLogger().setLevel(logging.CRITICAL)  # silence root logger
    unittest.main(verbosity=2)
