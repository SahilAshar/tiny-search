from uuid import UUID
from src.schemas.output import Document

K1_CONSTANT = 1.2
B_CONSTANT = 0.75
AVG_DOC_LENGTH = 500

InvertedIndex = dict[str, list[tuple[UUID, int]]]
DocumentStore = dict[UUID, Document]
