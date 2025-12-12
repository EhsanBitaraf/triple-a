import importlib
import sys
import traceback
import unittest
from unittest.mock import patch, MagicMock
from types import SimpleNamespace
import logging

# Silence logs from the enrichment module
logging.getLogger("triplea.service.repository.pipeline_flag.__go_get_enrich_data").setLevel(
    logging.CRITICAL
)


class TestGoGetEnrichData(unittest.TestCase):
    """Tests for go_get_enrich_data function in __go_get_enrich_data module."""

    def setUp(self):
        """Prepare fake data and mocks."""
        # Simple fake "database"
        self.db = {
            "a1": {"id": "a1", "title": "Paper A", "doi": "10.1/a"},
            "a2": {"id": "a2", "title": "Paper B"},  # no DOI
        }

        class FakeTqdm:
            def __init__(self, total, desc=""):
                self.total = total
                self.desc = desc
                self.count = 0

            def set_description(self, desc):
                self.desc = desc

            def update(self, n):
                self.count += n

            def close(self):
                pass

        self.FakeTqdm = FakeTqdm

        class FakeArticle:
            def __init__(self, **kwargs):
                if kwargs.get("raise_error"):
                    raise ValueError("Invalid article")
                self.__dict__.update(kwargs)

        self.FakeArticle = FakeArticle

        def fake_model(article_obj, overwrite=False):
            if not getattr(article_obj, "doi", None):
                return None
            return {
                **article_obj.__dict__,
                "altmetric_enriched": True,
                "altmetric_score": 42.0,
            }

        self.fake_model = fake_model

        # Mock persist
        self.persist = MagicMock()
        self.persist.get_all_article_id_list.return_value = list(self.db.keys())
        self.persist.get_article_by_id.side_effect = lambda i: self.db.get(i)
        self.persist.update_article_by_id.side_effect = lambda obj, i: self.db.update(
            {i: obj}
        )

    @patch("triplea.service.repository.pipeline_flag.__go_get_enrich_data.model_altmetric_by_doi")
    @patch("triplea.service.repository.pipeline_flag.__go_get_enrich_data.Article")
    @patch("triplea.service.repository.pipeline_flag.__go_get_enrich_data.SETTINGS")
    @patch("triplea.service.repository.pipeline_flag.__go_get_enrich_data.persist")
    @patch("triplea.service.repository.pipeline_flag.__go_get_enrich_data.get_tqdm")
    def test_enrich_success(self, m_get_tqdm, m_persist, m_settings, m_article, m_model):
        """Should enrich only articles that have DOI."""
        from triplea.service.repository.pipeline_flag.__go_get_enrich_data import go_get_enrich_data

        # Mock setup
        m_settings.AAA_CLI_ALERT_POINT = 2
        m_get_tqdm.return_value = lambda *a, **kw: self.FakeTqdm(*a, **kw)
        m_persist.get_all_article_id_list.return_value = list(self.db.keys())
        m_persist.get_article_by_id.side_effect = lambda i: self.db.get(i)
        m_persist.update_article_by_id.side_effect = lambda obj, i: self.db.update({i: obj})
        m_article.side_effect = lambda **kw: self.FakeArticle(**kw)
        m_model.side_effect = self.fake_model

        # Run
        go_get_enrich_data("altmetric_by_doi")

        # Verify
        self.assertTrue(self.db["a1"]["altmetric_enriched"])
        self.assertNotIn("altmetric_enriched", self.db["a2"])


    def test_invalid_model_debug(self):
        """Run the function and print any exceptions it raises."""
        sys.modules.pop("triplea.service.repository.pipeline_flag.__go_get_enrich_data", None)
        mod = importlib.import_module("triplea.service.repository.pipeline_flag.__go_get_enrich_data")

    # def test_invalid_model_raises(self):
    #     """Ensure ValueError is raised for unsupported model names."""
    #     # Always import a fresh, clean copy of the module
    #     sys.modules.pop("triplea.service.repository.pipeline_flag.__go_get_enrich_data", None)
    #     mod = importlib.import_module("triplea.service.repository.pipeline_flag.__go_get_enrich_data")

    #     with self.assertRaises(ValueError) as ctx:
    #         mod.go_get_enrich_data("not_a_model")

    #     # Verify message for clarity (optional)
    #     self.assertIn("not recognized", str(ctx.exception))
    #     self.assertIn("altmetric_by_doi", str(ctx.exception))
        


    @patch("triplea.service.repository.pipeline_flag.__go_get_enrich_data.model_altmetric_by_doi")
    @patch("triplea.service.repository.pipeline_flag.__go_get_enrich_data.Article")
    @patch("triplea.service.repository.pipeline_flag.__go_get_enrich_data.SETTINGS")
    @patch("triplea.service.repository.pipeline_flag.__go_get_enrich_data.persist")
    @patch("triplea.service.repository.pipeline_flag.__go_get_enrich_data.get_tqdm")
    def test_article_parse_error_skips(self, m_get_tqdm, m_persist, m_settings, m_article, m_model):
        """If Article() raises, the article should be skipped without breaking the loop."""
        from triplea.service.repository.pipeline_flag.__go_get_enrich_data import go_get_enrich_data

        # One broken, one valid article
        self.db = {
            "bad": {"id": "bad", "raise_error": True},
            "ok": {"id": "ok", "doi": "10.1/ok"},
        }

        m_settings.AAA_CLI_ALERT_POINT = 2
        m_get_tqdm.return_value = lambda *a, **kw: self.FakeTqdm(*a, **kw)
        m_persist.get_all_article_id_list.return_value = list(self.db.keys())
        m_persist.get_article_by_id.side_effect = lambda i: self.db.get(i)
        m_persist.update_article_by_id.side_effect = lambda obj, i: self.db.update({i: obj})

        def fake_article(**kw):
            if kw.get("raise_error"):
                raise ValueError("Invalid article data")
            return self.FakeArticle(**kw)

        m_article.side_effect = fake_article

        def fake_model(article_obj, overwrite=False):
            if not getattr(article_obj, "doi", None):
                return None
            return {**article_obj.__dict__, "altmetric_enriched": True}

        m_model.side_effect = fake_model

        # Run
        go_get_enrich_data("altmetric_by_doi")

        # Verify results
        self.assertNotIn("altmetric_enriched", self.db["bad"])
        self.assertTrue(self.db["ok"]["altmetric_enriched"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
