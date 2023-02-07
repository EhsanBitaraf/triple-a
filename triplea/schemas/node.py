from pydantic import BaseModel,Field
from typing import Optional


class Node(BaseModel):
    Type: Optional[str]  =  Field(description='')
    Identifier: Optional[str]  =  Field(description='')
    Name: Optional[str]  =  Field(description='')

class Edge(BaseModel):
    HashID: Optional[str]  =  Field(description='')
    SourceID: Optional[str]  =  Field(description='')
    DestinationID: Optional[str]  =  Field(description='')
    Type: Optional[str]  =  Field(description='')




