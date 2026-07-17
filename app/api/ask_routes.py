from fastapi import APIRouter

from app.schemas.ask_schema import AskRequest
from app.services.retriever_service import RetrieverService

router = APIRouter()

retriever = RetrieverService()


@router.post("/ask")
def ask(request: AskRequest):

    return retriever.ask(
        request.question
    )