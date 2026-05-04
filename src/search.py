from index.indexer import IndexClient
from index.scoring import ScoringClient
from src.schemas.output import ScoredDocument


class SearchClient:
    def __init__(
        self, index_client: IndexClient, scoring_client: ScoringClient
    ) -> None:
        self._index_client = index_client
        self._scoring_client = scoring_client

    def search(self, query: str, limit: int) -> list[ScoredDocument]:
        tokenizer = self._index_client.get_tokenizer()
        query_tokens = tokenizer.tokenize(query)

        scored_ids = self._scoring_client.score(query_tokens, limit, self._index_client)

        doc_store = self._index_client.get_doc_store()
        return [
            ScoredDocument(document=doc_store[doc_id], score=score)
            for doc_id, score in scored_ids
        ]
