from collections import Counter
from pathlib import Path
from uuid import UUID, uuid5, NAMESPACE_URL

from index.tokenizer import TokenizerClient
from index.types import DocumentStore, InvertedIndex
from src.schemas.output import Document
from utils.file_utils import validate_file_path


class IndexClient:
    _instance: "IndexClient | None" = None

    def __new__(cls) -> "IndexClient":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._index = {}
            cls._instance._doc_store = {}
            cls._instance._tokenizer = TokenizerClient()
        return cls._instance

    _index: InvertedIndex
    _doc_store: DocumentStore
    _tokenizer: TokenizerClient

    def get_index(self) -> InvertedIndex:
        return self._index

    def get_doc_store(self) -> DocumentStore:
        return self._doc_store

    def get_tokenizer(self) -> TokenizerClient:
        return self._tokenizer

    def ingest(self, path: Path) -> UUID:
        validate_file_path(path)

        doc_id = uuid5(NAMESPACE_URL, str(path))
        content = path.read_text(encoding="utf-8")

        self._doc_store[doc_id] = Document(
            id=doc_id,
            path=path,
            name=path.name,
            size=path.stat().st_size,
            file_type=path.suffix,
        )

        tokens = self._tokenizer.tokenize(content)
        counts = Counter(tokens)

        for token, count in counts.items():
            if token not in self._index:
                self._index[token] = []
            self._index[token].append((doc_id, count))

        return doc_id
