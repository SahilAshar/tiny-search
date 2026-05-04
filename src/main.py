from fastapi import Depends, FastAPI, HTTPException
from index.main import IndexClient
from src.schemas.input import IngestRequest, SearchRequest
from src.schemas.output import IngestResponse, SearchResponse
from utils.file_utils import PathNotFoundError, InvalidFileError

app = FastAPI()
index_client = IndexClient()


@app.get("/search", response_model=SearchResponse)
async def search(request: SearchRequest = Depends()) -> SearchResponse:
    results = index_client.search(request.query, request.limit)
    return SearchResponse(results=results)


@app.post("/ingest", response_model=IngestResponse, status_code=200)
async def ingest(request: IngestRequest) -> IngestResponse:
    try:
        doc_id = index_client.ingest(request.path)
    except PathNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidFileError as e:
        raise HTTPException(status_code=422, detail=str(e))

    return IngestResponse(id=doc_id)
