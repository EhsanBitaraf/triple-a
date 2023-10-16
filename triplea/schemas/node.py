from pydantic import BaseModel, Field
from typing import Optional

# custom_encoder = lambda obj:  dict(_type=type(obj).__name__, **obj.dict())


# It creates a class called Node with the following attributes:
#  Type, Identifier, and Name.
class Node(BaseModel):
    Type: Optional[str] = Field(description="")
    Identifier: Optional[str] = Field(description="")
    Name: Optional[str] = Field(description="")

    # def toJSON(self):
    #     return json.dumps(self, default=lambda o: o.__dict__,
    #         sort_keys=True, indent=4)

    def json(self):
        return {"Type": self.Type,
                "Identifier": self.Identifier,
                "Name": self.Name}

    # class Config:
    #     json_encoders = {
    #         Base: custom_encoder
    #     }


# The Edge class is a model that has four fields:
#  HashID, SourceID, DestinationID, and Type
class Edge(BaseModel):
    HashID: Optional[str] = Field(description="")
    SourceID: Optional[str] = Field(description="")
    DestinationID: Optional[str] = Field(description="")
    Type: Optional[str] = Field(description="")
    Weight: Optional[float] = Field(description="")
