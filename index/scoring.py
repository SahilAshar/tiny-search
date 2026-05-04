from math import log
from uuid import UUID

from index.indexer import IndexClient
from index.types import (
    InvertedIndex,
    DocumentStore,
    AVG_DOC_LENGTH,
    B_CONSTANT,
    K1_CONSTANT,
)
from src.schemas.output import Document


class ScoringClient:
    def IDF(self, term: str, index: InvertedIndex, doc_store: DocumentStore) -> float:
        return log(len(doc_store) / len(index[term]))

    def score(
        self,
        query_tokens: list[str],
        limit: int,
        index_client: IndexClient,
    ) -> list[tuple[UUID, float]]:
        index = index_client.get_index()
        doc_store = index_client.get_doc_store()

        doc_scores: dict[UUID, float] = {}

        # for each term, get all matching docs, and score per doc
        # doc score is += per term
        # return final score sorting docs across all query terms

        for term in query_tokens:
            if term not in index:
                continue
            doc_list = index[term]

            for doc_id, term_freq in doc_list:
                doc: Document = doc_store[doc_id]
                k_derived = K1_CONSTANT * (
                    1 - B_CONSTANT + B_CONSTANT * doc.size / AVG_DOC_LENGTH
                )
                tf_adjusted = (term_freq) / (term_freq + k_derived)
                score = self.IDF(term, index, doc_store) * tf_adjusted

                doc_scores[doc_id] = doc_scores.get(doc_id, 0.0) + score

        sorted_docs = sorted(doc_scores.items(), key=lambda d: d[1], reverse=True)
        return sorted_docs[:limit]
