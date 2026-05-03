from pathlib import Path

from index.types import InvertedIndex


class IndexClient:
    _instance: "IndexClient | None" = None

    def __new__(cls) -> "IndexClient":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._index = {}
        return cls._instance

    _index: InvertedIndex

    def get_index(self) -> InvertedIndex:
        return self._index

    def ingest(self, path: Path) -> str:
        content = path.read_text(encoding="utf-8")

        # TODO: tokenize content
        # TODO: store in inverted index

        return content
