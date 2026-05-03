from fastapi import FastAPI
from src.models import SearchResponse

app = FastAPI()


@app.get("/search", response_model=SearchResponse)
async def search(query: str) -> SearchResponse:
    return SearchResponse(results=[])
