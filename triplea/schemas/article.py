from pydantic import BaseModel,Field
from typing import Optional


class Article(BaseModel):
    PMID: Optional[str]  =  Field(description='')
    Title: Optional[str]  =  Field(description='')
    OreginalArticle : Optional[dict] =  Field(description='')
    state : Optional[int] =   Field(description='')