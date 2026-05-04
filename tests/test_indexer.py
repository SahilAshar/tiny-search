import pytest
from pathlib import Path
from uuid import uuid5, NAMESPACE_URL

from index.indexer import IndexClient


@pytest.fixture(autouse=True)
def reset_singleton() -> None:
    IndexClient._instance = None


@pytest.fixture
def sample_file(tmp_path: Path) -> Path:
    f = tmp_path / "doc.txt"
    f.write_text("Python search engine building blocks")
    return f


def test_ingest_returns_deterministic_id(sample_file: Path) -> None:
    client = IndexClient()
    doc_id = client.ingest(sample_file)
    expected = uuid5(NAMESPACE_URL, str(sample_file))
    assert doc_id == expected


def test_ingest_populates_index(sample_file: Path) -> None:
    client = IndexClient()
    client.ingest(sample_file)
    index = client.get_index()
    assert len(index) > 0


def test_ingest_populates_doc_store(sample_file: Path) -> None:
    client = IndexClient()
    doc_id = client.ingest(sample_file)
    doc_store = client.get_doc_store()
    assert doc_id in doc_store
    assert doc_store[doc_id].name == "doc.txt"


def test_ingest_nonexistent_file() -> None:
    client = IndexClient()
    with pytest.raises(Exception):
        client.ingest(Path("/nonexistent/file.txt"))


def test_ingest_multiple_files(tmp_path: Path) -> None:
    f1 = tmp_path / "a.txt"
    f1.write_text("python programming language")
    f2 = tmp_path / "b.txt"
    f2.write_text("search engine optimization")

    client = IndexClient()
    id1 = client.ingest(f1)
    id2 = client.ingest(f2)

    assert id1 != id2
    assert len(client.get_doc_store()) == 2
