# cyberstory/ai/schemas.py
from pydantic import BaseModel
from typing import List, Optional

class Character(BaseModel):
    name: str
    description: str
    faction: str

class Object(BaseModel):
    name: str
    description: str
    tags: List[str]

class Threat(BaseModel):
    name: str
    description: str
    hits: int
    tags: List[str]

class Scene(BaseModel):
    name: str
    description: str
    characters: List[Character]
    objects: List[Object]
    threats: List[Threat]
    objectives: List[str]
    suggested_actions: List[str]
    completed: bool

# Hier könntest du weitere Modelle für Quests, Aktionen, Konsequenzen usw. definieren