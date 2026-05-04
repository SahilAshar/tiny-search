# tiny-search

A BM25 search engine built from scratch in Python. No Solr, no Elasticsearch, no libraries for scoring — just the raw math.

Built as a learning project to understand information retrieval from first principles: tokenization, inverted indexes, TF-IDF, and BM25 scoring.

## How it works

1. **Ingest** a document via `POST /ingest` with a file path
2. **Tokenize** the content (word splitting, stop word removal, Porter stemming via NLTK)
3. **Index** tokens into an in-memory inverted index (`term → [(doc_id, count)]`)
4. **Search** via `GET /search?query=...&limit=10` — tokenizes the query, scores every matching document using BM25, returns ranked results

### BM25 scoring

Each document is scored per query term using:

```
score(term, doc) = IDF(term) * tf / (tf + K)
```

Where:
- **IDF** = `log(total_docs / docs_containing_term)` — rare terms score higher
- **tf** = term frequency in the document
- **K** = `k1 * (1 - b + b * doc_len / avg_doc_len)` — saturation constant adjusted for document length
- **k1** (default 1.2) controls term frequency saturation
- **b** (default 0.75) controls document length normalization

Final document score is the sum across all query terms.

## Quick start

```bash
make all       # create venv, install deps, lint, test
make run       # start the server (http://localhost:8000)
```

Swagger UI is available at `http://localhost:8000/docs`.

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/ingest` | Index a document by file path |
| `GET` | `/search` | Search indexed documents |

### Ingest

```bash
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{"path": "/path/to/document.md"}'
```

### Search

```bash
curl "http://localhost:8000/search?query=your+search+terms&limit=10"
```

## Project structure

```
src/
  main.py              # FastAPI app and endpoints
  search.py            # SearchClient — orchestrates index + scoring
  schemas/
    input.py           # Request schemas (SearchRequest, IngestRequest)
    output.py          # Response schemas (Document, SearchResponse)
index/
  indexer.py           # IndexClient — inverted index and document store
  scoring.py           # ScoringClient — BM25 implementation
  tokenizer.py         # TokenizerClient — NLTK tokenization + stemming
  types.py             # Shared type aliases and constants
utils/
  file_utils.py        # File validation with custom exceptions
bin/
  nltk/                # Vendored NLTK data (tokenizer + stopwords)
```

## Roadmap

- [ ] Persistent storage (SQLite) so the index survives restarts
- [ ] Computed average document length (currently hardcoded)
- [ ] Semantic search (embeddings + vector index)
- [ ] Hybrid scoring (BM25 + semantic)
- [ ] Query expansion and re-ranking
- [ ] Evaluation framework (precision, recall, nDCG)
