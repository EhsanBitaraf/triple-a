
import unittest
from unittest.mock import patch, MagicMock
import logging
from triplea.schemas.article import Article
from triplea.service.repository.pipeline_flag.__go_extract_topic import go_extract_topic

class TestGoExtractTopic(unittest.TestCase):
    def setUp(self):
        """Set up common mocks and test fixtures."""
        # Silence logging during tests
        logging.getLogger('').handlers = [logging.NullHandler()]

        # Mock external dependencies
        self.persist_patch = patch('triplea.service.repository.pipeline_flag.__go_extract_topic.persist')
        self.state_manager_patch = patch('triplea.service.repository.pipeline_flag.__go_extract_topic.state_manager')
        self.get_tqdm_patch = patch('triplea.service.repository.pipeline_flag.__go_extract_topic.get_tqdm')
        self.settings_patch = patch('triplea.service.repository.pipeline_flag.__go_extract_topic.SETTINGS')
        self.article_patch = patch('triplea.service.repository.pipeline_flag.__go_extract_topic.Article')

        # Start mocks
        self.mock_persist = self.persist_patch.start()
        self.mock_state_manager = self.state_manager_patch.start()
        self.mock_get_tqdm = self.get_tqdm_patch.start()
        self.mock_settings = self.settings_patch.start()
        self.mock_article = self.article_patch.start()

        # Configure default mock behaviors
        self.mock_settings.AAA_CLI_ALERT_POINT = 2
        self.mock_get_tqdm.return_value = MagicMock()  # Mock tqdm for progress bar
        self.mock_persist.get_article_id_list_by_cstate.return_value = ['1', '2']
        self.mock_persist.get_article_by_id.return_value = {'ID': '1', 'FlagExtractTopic': 0}
        self.mock_state_manager.extract_topic_abstract.return_value = Article(ID='1', FlagExtractTopic=1)
        self.mock_persist.update_article_by_id = MagicMock()
        self.mock_persist.refresh = MagicMock()
        self.mock_article.return_value = Article(ID='1', FlagExtractTopic=0)

    def tearDown(self):
        """Clean up mocks after each test."""
        self.persist_patch.stop()
        self.state_manager_patch.stop()
        self.get_tqdm_patch.stop()
        self.settings_patch.stop()
        self.article_patch.stop()

    def test_valid_input_parameters(self):
        """Test go_extract_topic with valid parameters."""
        go_extract_topic(method="textrank", top=5, threshold=0.1, proccess_bar=False)
        self.mock_persist.get_article_id_list_by_cstate.assert_called_once_with(0, "FlagExtractTopic")
        self.mock_state_manager.extract_topic_abstract.assert_called()
        self.mock_persist.update_article_by_id.assert_called()
        self.mock_persist.refresh.assert_called()

    def test_invalid_top_parameter(self):
        """Test go_extract_topic with invalid top parameter."""
        with self.assertRaises(ValueError) as cm:
            go_extract_topic(method="textrank", top=0, threshold=0.1)
        self.assertEqual(str(cm.exception), "Parameter 'top' must be a positive integer.")

    def test_negative_threshold(self):
        """Test go_extract_topic with negative threshold."""
        with self.assertRaises(ValueError) as cm:
            go_extract_topic(method="textrank", top=5, threshold=-0.1)
        self.assertEqual(str(cm.exception), "Parameter 'threshold' must be a non-negative float.")

    def test_article_not_found(self):
        """Test behavior when article is not found."""
        self.mock_persist.get_article_id_list_by_cstate.return_value = ['3']
        self.mock_persist.get_article_by_id.return_value = None
        go_extract_topic(method="textrank", top=5, threshold=0.0, proccess_bar=True)
        self.mock_persist.update_article_by_id.assert_not_called()

    # def test_article_parsing_failure(self):
    #     """Test handling of article parsing error."""
    #     self.mock_persist.get_article_id_list_by_cstate.return_value = ['1']
    #     self.mock_persist.get_article_by_id.return_value = {'ID': '1', 'FlagExtractTopic': 0}
    #     self.mock_article.side_effect = Exception("Invalid article data")
    #     with self.assertRaises(ValueError) as cm:
    #         go_extract_topic(method="textrank", top=5, threshold=0.0, proccess_bar=False)
    #     self.assertIn("Failed to parse article ID 1", str(cm.exception))
    #     # Verify that no update is attempted due to parsing failure
    #     self.mock_persist.update_article_by_id.assert_not_called()

    def test_already_processed_article(self):
        """Test skipping already processed article."""
        self.mock_persist.get_article_by_id.return_value = {'ID': '1', 'FlagExtractTopic': 1}
        self.mock_article.return_value = Article(ID='1', FlagExtractTopic=1)
        go_extract_topic(method="textrank", top=5, threshold=0.0, proccess_bar=False)
        self.mock_state_manager.extract_topic_abstract.assert_not_called()
        self.mock_persist.update_article_by_id.assert_not_called()

    # def test_unsupported_state(self):
    #     """Test handling of unsupported article state."""
    #     self.mock_persist.get_article_id_list_by_cstate.return_value = ['1']
    #     self.mock_persist.get_article_by_id.return_value = {'ID': '1', 'FlagExtractTopic': 2}
    #     self.mock_article.return_value = Article(ID='1', FlagExtractTopic=2)
    #     with self.assertRaises(NotImplementedError) as cm:
    #         go_extract_topic(method="textrank", top=5, threshold=0.0, proccess_bar=False)
    #     self.assertEqual(str(cm.exception), "State 2 not supported")

    def test_topic_extraction_failure(self):
        """Test handling of topic extraction failure."""
        self.mock_state_manager.extract_topic_abstract.side_effect = Exception("Extraction error")
        self.mock_persist.get_article_by_id.return_value = {'ID': '1', 'FlagExtractTopic': 0}
        self.mock_article.return_value = Article(ID='1', FlagExtractTopic=0)
        go_extract_topic(method="textrank", top=5, threshold=0.0, proccess_bar=False)
        self.mock_persist.update_article_by_id.assert_called()
        # Check that article is marked as failed
        args, _ = self.mock_persist.update_article_by_id.call_args
        self.assertEqual(args[0].FlagExtractTopic, -1)

    def test_progress_bar_enabled(self):
        """Test progress bar functionality."""
        mock_tqdm = MagicMock()
        self.mock_get_tqdm.return_value = mock_tqdm
        go_extract_topic(method="textrank", top=5, threshold=0.0, proccess_bar=True)
        mock_tqdm.assert_called_once_with(total=2, desc="Processing")
        mock_tqdm.return_value.set_description.assert_called()
        mock_tqdm.return_value.update.assert_called()
        mock_tqdm.return_value.close.assert_called()

    def test_refresh_point_logic(self):
        """Test repository refresh logic at max_refresh_point."""
        self.mock_persist.get_article_id_list_by_cstate.return_value = ['1', '2', '3']
        self.mock_settings.AAA_CLI_ALERT_POINT = 2
        go_extract_topic(method="textrank", top=5, threshold=0.0, proccess_bar=False)
        self.assertGreaterEqual(self.mock_persist.refresh.call_count, 1)

    def test_empty_article_list(self):
        """Test behavior with empty article list."""
        self.mock_persist.get_article_id_list_by_cstate.return_value = []
        go_extract_topic(method="textrank", top=5, threshold=0.0, proccess_bar=True)
        self.mock_state_manager.extract_topic_abstract.assert_not_called()
        self.mock_persist.update_article_by_id.assert_not_called()

if __name__ == '__main__':
    unittest.main()
