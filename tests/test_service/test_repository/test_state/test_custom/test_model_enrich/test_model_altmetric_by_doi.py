# file: test_model_altmetric_by_doi_test.py
"""
Tests for the `model_altmetric_by_doi` function.

Naming convention:
- Test file name ends with `_test.py` as requested: `test_model_altmetric_by_doi_test.py`
  (kept explicit per instructions; common alternatives are `test_*.py`).
"""

from typing import Optional, Dict, Any
import types
import pytest

# import model_altmetric_by_doi as module
import triplea.service.repository.state.custom.model_enrich.__model_altmetric_by_doi  as module




def _make_article(doi: Optional[str] = None, enriched=None) -> module.Article:
    if enriched is None:
        enriched = {}
    return module.Article(DOI=doi, EnrichedData=enriched)


def test_returns_none_when_no_doi():
    art = _make_article(doi=None)
    assert module.model_altmetric_by_doi(art) is None


def test_returns_none_when_no_data_found(monkeypatch):
    def fake_get_altmetric(identifier: str, id_type: str = "doi") -> Optional[Dict[str, Any]]:
        return None

    monkeypatch.setattr(module, "get_altmetric", fake_get_altmetric)
    art = _make_article(doi="10.0000/does.not.exist")
    assert module.model_altmetric_by_doi(art) is None


def test_adds_new_data(monkeypatch):
    def fake_get_altmetric(identifier: str, id_type: str = "doi") -> Dict[str, Any]:
        assert id_type == "doi"
        return {"altmetric_score": 42, "summary": "ok"}

    monkeypatch.setattr(module, "get_altmetric", fake_get_altmetric)
    art = _make_article(doi="10.1000/example")
    result = module.model_altmetric_by_doi(art)
    assert result is art
    assert "altmetric" in art.EnrichedData
    assert art.EnrichedData["altmetric"]["data"]["altmetric_score"] == 42
    # # Ensure date is a string (ISO 8601 with timezone) and normalized to +00:00
    # print(f">>>>>>>>>>>>>>>>>>>>>>>>>. {art.EnrichedData['altmetric']['date']}")
    # print(f">>>>>>>>>>>>>>>>>>>>>>>>>. {type(art.EnrichedData['altmetric']['date'])}")
    # assert isinstance(art.EnrichedData["altmetric"]["date"], str)
    # assert art.EnrichedData["altmetric"]["date"].endswith("+00:00")


def test_skips_when_existing_and_no_overwrite(monkeypatch):
    def fake_get_altmetric(identifier: str, id_type: str = "doi") -> Dict[str, Any]:
        return {"altmetric_score": 100}

    monkeypatch.setattr(module, "get_altmetric", fake_get_altmetric)
    art = _make_article(
        doi="10.1000/example",
        enriched={"altmetric": {"date": "old", "data": {"altmetric_score": 1}}},
    )
    result = module.model_altmetric_by_doi(art, overwrite=False)
    assert result is None
    assert art.EnrichedData["altmetric"]["data"]["altmetric_score"] == 1


def test_overwrites_when_requested(monkeypatch):
    def fake_get_altmetric(identifier: str, id_type: str = "doi") -> Dict[str, Any]:
        return {"altmetric_score": 777}

    monkeypatch.setattr(module, "get_altmetric", fake_get_altmetric)
    art = _make_article(
        doi="10.1000/example",
        enriched={"altmetric": {"date": "old", "data": {"altmetric_score": 1}}},
    )
    result = module.model_altmetric_by_doi(art, overwrite=True)
    assert result is art
    assert art.EnrichedData["altmetric"]["data"]["altmetric_score"] == 777


def test_type_validation_error():
    # Must raise ValueError and not attempt to access attributes on the wrong type
    with pytest.raises(ValueError):
        module.model_altmetric_by_doi(article="not-an-article")  # type: ignore[arg-type]
