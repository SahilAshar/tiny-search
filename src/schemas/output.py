from pathlib import Path
from uuid import UUID

from pydantic import BaseModel


class Document(BaseModel):
    id: UUID
    path: Path
    name: str
    size: int
    file_type: str


class SearchResponse(BaseModel):
    results: list[Document]
