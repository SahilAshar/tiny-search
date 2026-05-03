from pathlib import Path


def ingest(path: Path) -> str:
    content = path.read_text(encoding="utf-8")

    # TODO: tokenize content
    # TODO: store in inverted index

    return content
