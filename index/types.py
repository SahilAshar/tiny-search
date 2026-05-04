from uuid import UUID
from src.schemas.output import Document

InvertedIndex = dict[str, list[tuple[UUID, int]]]
DocumentStore = dict[UUID, Document]
