from pydantic import BaseModel, Field
from typing import Optional
import enum


class NamedEntity(BaseModel):
    Label: Optional[str] = Field(description="")
    Entity: Optional[str] = Field(description="")


class Keyword(BaseModel):
    Text: Optional[str] = Field(description="")
    IS_Major: Optional[bool] = Field(
        description="""The MajorTopic attribute is set to True (for Yes)
        when the MeSH Heading/Keyword alone is
        a central concept of the article"""
    )
    IS_Mesh: Optional[bool] = Field(description="")


class AffiliationParseMethod(enum.IntEnum):
    SIMPLE_PARSE = 1
    TITIPATA_API = 2  # https://github.com/titipata/affiliation_parser


class Affiliation(BaseModel):
    HashID: Optional[str]
    Text: Optional[str] = Field(description="")
    Part1: Optional[str] = Field(description="")
    Part2: Optional[str] = Field(description="")
    Part3: Optional[str] = Field(description="")
    Part4: Optional[str] = Field(description="")
    Part5: Optional[str] = Field(description="")
    Part6: Optional[str] = Field(description="")
    Has_Extra: Optional[bool] = Field(description="")
    Structural: Optional[list[dict]] = Field(description="")
    ParseMethod: Optional[AffiliationParseMethod] = Field(description="")


class Author(BaseModel):
    HashID: Optional[str]
    LastName: Optional[str] = Field(
        description="""contains the surname or the single name used by
        an individual, even if that single name
          is not considered to be a surname"""
    )
    ForeName: Optional[str] = Field(
        description="contains the remainder of name except for suffix"
    )
    FullName: Optional[str] = Field(description="")
    ORCID: Optional[str] = Field(description="")
    Affiliations: Optional[list[Affiliation]] = Field(description="")


class Article(BaseModel):
    PMID: Optional[str] = Field(
        description="""the PubMed (NLM database that incorporates MEDLINE)
          unique identifier, is a 1 to 8-digit accession number
          with no leading zeros."""
    )
    DOI: Optional[str] = Field(description="")
    PMC: Optional[str] = Field(
        description="""This is a unique reference number or identifier
        that is assigned to every article that is accepted into PMC."""
    )
    Title: Optional[str] = Field(
        description="""Article Title contains the entire title of
        the journal article. Article Title is always in English;
          those titles originally published in a non-English language
            and translated for Article Title are enclosed
            in square brackets."""
    )
    Journal: Optional[str] = Field(
        description="""The full journal title
        (taken from NLM cataloging data following NLM rules
        for how to compile a serial name) is exported in this element."""
    )
    Authors: Optional[list[Author]] = Field(description="")
    Abstract: Optional[str] = Field(description="")
    OreginalArticle: Optional[dict] = Field(description="")
    State: Optional[int] = Field(description="")
    QueryTranslation: Optional[str] = Field(description="")
    Keywords: Optional[list[Keyword]] = Field(description="")
    Topics: Optional[list[dict]] = Field(description="")
    References: Optional[list[str]] = Field(description="")
    CitedBy: Optional[list[str]] = Field(description="")
    InsertType: Optional[list[str]] = Field(description="")
    ReferenceCrawlerDeep: Optional[int] = Field(description="")
    CiteCrawlerDeep: Optional[int] = Field(description="")
    NamedEntities: Optional[list[NamedEntity]] = Field(description="")
    FlagExtractKG: Optional[int] = Field(description="")
    FlagAffiliationMining: Optional[int] = Field(description="")
    FlagExtractTopic: Optional[int] = Field(description="")
