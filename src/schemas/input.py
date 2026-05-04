from pathlib import Path

from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    limit: int = 10


class IngestRequest(BaseModel):
    path: Path
