from uuid import UUID

from index.types import InvertedIndex


class ScoringClient:
    def score(
        self, query_tokens: list[str], limit: int, index: InvertedIndex
    ) -> list[UUID]:
        # TODO: implement BM25 scoring

        return []
