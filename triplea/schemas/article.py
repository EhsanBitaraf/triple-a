from pydantic import BaseModel, Field
from typing import Optional
import enum
from datetime import datetime


class NamedEntity(BaseModel):
    Label: Optional[str] = Field(description="", default=None)
    Entity: Optional[str] = Field(description="", default=None)


class Keyword(BaseModel):
    Text: Optional[str] = Field(description="", default=None)
    IS_Major: Optional[bool] = Field(
        description="""The MajorTopic attribute is set to True (for Yes)
        when the MeSH Heading/Keyword alone is
        a central concept of the article""",
        default=None,
    )
    IS_Mesh: Optional[bool] = Field(description="", default=None)


class AffiliationParseMethod(enum.IntEnum):
    SIMPLE_PARSE = 1
    TITIPATA_API = 2  # https://github.com/titipata/affiliation_parser
    REGEX_API = 3     # It is my API with affparsmodels package


class SourceBankType(enum.IntEnum):
    PUBMED = 1
    ARXIV = 2
    WOS = 3
    SCOPUS = 4
    IEEE = 5
    UNKNOWN = 6
    GOOGLESCHOLAR = 7
    EMBASE = 8
    ACM = 9


class Affiliation(BaseModel):
    HashID: Optional[str] = Field(description="", default=None)
    Text: Optional[str] = Field(description="", default=None)
    Part1: Optional[str] = Field(description="", default=None)
    Part2: Optional[str] = Field(description="", default=None)
    Part3: Optional[str] = Field(description="", default=None)
    Part4: Optional[str] = Field(description="", default=None)
    Part5: Optional[str] = Field(description="", default=None)
    Part6: Optional[str] = Field(description="", default=None)
    Has_Extra: Optional[bool] = Field(description="", default=None)
    Structural: Optional[list[dict]] = Field(description="", default=None)
    ParseMethod: Optional[AffiliationParseMethod] = Field(description="", default=None)


class Author(BaseModel):
    HashID: Optional[str] = Field(description="", default=None)
    LastName: Optional[str] = Field(
        description="""contains the surname or the single name used by
        an individual, even if that single name
          is not considered to be a surname""",
        default=None,
    )
    ForeName: Optional[str] = Field(
        description="contains the remainder of name except for suffix", default=None
    )
    FullName: Optional[str] = Field(description="", default=None)
    ORCID: Optional[str] = Field(description="", default=None)
    Affiliations: Optional[list[Affiliation]] = Field(description="", default=None)


class Article(BaseModel):
    SourceBank: Optional[SourceBankType] = Field(description="", default=None)
    PMID: Optional[str] = Field(
        description="""the PubMed (NLM database that incorporates MEDLINE)
          unique identifier, is a 1 to 8-digit accession number
          with no leading zeros.""",
        default=None,
    )
    DOI: Optional[str] = Field(description="", default=None)
    PMC: Optional[str] = Field(
        description="""This is a unique reference number or identifier
        that is assigned to every article that is accepted into PMC.""",
        default=None,
    )
    Title: Optional[str] = Field(
        description="""Article Title contains the entire title of
        the journal article. Article Title is always in English;
          those titles originally published in a non-English language
            and translated for Article Title are enclosed
            in square brackets.""",
        default=None,
    )
    Journal: Optional[str] = Field(
        description="""The full journal title
        (taken from NLM cataloging data following NLM rules
        for how to compile a serial name) is exported in this element.""",
        default=None,
    )
    Authors: Optional[list[Author]] = Field(description="", default=None)
    Abstract: Optional[str] = Field(description="", default=None)
    OreginalArticle: Optional[dict] = Field(description="", default=None)
    State: Optional[int] = Field(description="", default=None)
    QueryTranslation: Optional[str] = Field(description="", default=None)
    Keywords: Optional[list[Keyword]] = Field(description="", default=None)
    Topics: Optional[list[dict]] = Field(description="", default=None)
    References: Optional[list[str]] = Field(description="", default=None)
    CitedBy: Optional[list[str]] = Field(description="", default=None)
    InsertType: Optional[list[str]] = Field(description="", default=None)
    ReferenceCrawlerDeep: Optional[int] = Field(description="", default=None)
    CiteCrawlerDeep: Optional[int] = Field(description="", default=None)
    NamedEntities: Optional[list[NamedEntity]] = Field(description="", default=None)
    FlagExtractKG: Optional[int] = Field(description="", default=0)
    FlagAffiliationMining: Optional[int] = Field(description="", default=0)
    FlagExtractTopic: Optional[int] = Field(description="", default=0)
    FlagEmbedding: Optional[int] = Field(description="", default=0)
    FlagShortReviewByLLM: Optional[int] = Field(description="", default=0)

    Published: Optional[datetime] = Field(description="", default=None)
    ArxivID: Optional[str] = Field(description="", default=None)

    FullTextMetadata: Optional[dict] = Field(description="", default=None)
    ReviewLLM: Optional[list[dict]] = Field(description="", default=None)
    AffiliationIntegration: Optional[list[dict]] = Field(
        description="""This field was created to unify affiliation
          between different formats of articles""",
        default=None,
    )
    CitationCount: Optional[int] = Field(
        description="""
Number of times the article has been cited, gathered from
external sources like PubMed or Scopus.
Retrieved from external sources (e.g., PubMed, Scopus) during processing
between steps 2 and 3. Used to quantify the article's scholarly impact.""",
        default=0,
    )
    Language: Optional[str] = Field(
        description="""Language""",
        default="",
    )
    Year: Optional[str] = Field(
        description="""(publication) year/date. RIS Tag : PY, Y1, YR  """,
        default="",
    )
    SerialNumber: Optional[str] = Field(
        description="""ISSN, ISBN, or report/document/patent number.
        RIS Tag : SN  """,
        default="",
    )
    links: Optional[str] = Field(
        description="""Links. RIS Tag : LK, UR  """,
        default= None,
    )
    PublicationType: Optional[list[str]] = Field(description="""
        """,
        default=None
    )
    EnrichedData: Optional[dict] = Field(description="", default=None)