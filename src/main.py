from fastapi import Depends, FastAPI
from src.schemas.input import SearchRequest
from src.schemas.output import SearchResponse

app = FastAPI()


@app.get("/search", response_model=SearchResponse)
async def search(request: SearchRequest = Depends()) -> SearchResponse:
    return SearchResponse(results=[])
