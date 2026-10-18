from pydantic import BaseModel, Field
from typing import Optional

class SessionCreate(BaseModel):
    title: str = Field(default="New conversation", max_length=120)

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=8000)
    session_id: Optional[str] = None

class EntityCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    entity_type: str = Field(default="Concept", max_length=80)
    description: str = Field(default="", max_length=2000)

class RelationshipCreate(BaseModel):
    source: str = Field(min_length=1, max_length=200)
    relation: str = Field(min_length=1, max_length=80)
    target: str = Field(min_length=1, max_length=200)
