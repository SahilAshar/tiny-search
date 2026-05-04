import pytest
from pathlib import Path

from index.indexer import IndexClient
from index.scoring import ScoringClient


@pytest.fixture(autouse=True)
def reset_singleton() -> None:
    IndexClient._instance = None


@pytest.fixture
def populated_index(tmp_path: Path) -> IndexClient:
    f1 = tmp_path / "python.txt"
    f1.write_text("python python python programming language")
    f2 = tmp_path / "search.txt"
    f2.write_text("search engine search retrieval search ranking")
    f3 = tmp_path / "mixed.txt"
    f3.write_text("python search engine building")

    client = IndexClient()
    client.ingest(f1)
    client.ingest(f2)
    client.ingest(f3)
    return client


def test_single_term_query(populated_index: IndexClient) -> None:
    scorer = ScoringClient()
    tokenizer = populated_index.get_tokenizer()
    tokens = tokenizer.tokenize("python")
    results = scorer.score(tokens, 10, populated_index)

    assert len(results) > 0
    assert all(isinstance(score, float) for _, score in results)


def test_results_sorted_descending(populated_index: IndexClient) -> None:
    scorer = ScoringClient()
    tokenizer = populated_index.get_tokenizer()
    tokens = tokenizer.tokenize("search")
    results = scorer.score(tokens, 10, populated_index)

    scores = [score for _, score in results]
    assert scores == sorted(scores, reverse=True)


def test_limit_respected(populated_index: IndexClient) -> None:
    scorer = ScoringClient()
    tokenizer = populated_index.get_tokenizer()
    tokens = tokenizer.tokenize("python search")
    results = scorer.score(tokens, 1, populated_index)

    assert len(results) == 1


def test_unknown_term_returns_empty(populated_index: IndexClient) -> None:
    scorer = ScoringClient()
    results = scorer.score(["xyznonexistent"], 10, populated_index)
    assert results == []


def test_multi_term_scores_higher(populated_index: IndexClient) -> None:
    scorer = ScoringClient()
    tokenizer = populated_index.get_tokenizer()

    single = scorer.score(tokenizer.tokenize("python"), 10, populated_index)
    multi = scorer.score(tokenizer.tokenize("python search"), 10, populated_index)

    single_top = single[0][1]
    multi_top = multi[0][1]
    assert multi_top >= single_top
