from typing import Optional, List, Set, Dict

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConnectionConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    host: str
    port: int
    database: str
    username: str
    password: str

class Movie(BaseModel):
    tconst: str
    title: str
    year: Optional[int]
    genres: Set[str]
    actor_names: List[str] = Field(default_factory=list)

class Actor(BaseModel):
    nconst: str
    name: str
    played_in: List = Field(default_factory=list)
    costar_name_to_count: Dict[str, int] = Field(default_factory=dict)
