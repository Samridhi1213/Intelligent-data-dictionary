from fastapi import APIRouter, Depends
from pydantic import BaseModel
from backend.services.ai_service import AIService
from backend.services.metadata_service import MetadataService
from backend.connectors.postgres import PostgresConnector
from backend.config import settings
import json

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

def get_postgres_connector():
    return PostgresConnector(settings.DATABASE_URL)

def get_metadata_service(connector = Depends(get_postgres_connector)):
    return MetadataService(connector)

# Global service instances
_ai_service = AIService()

def get_ai_service():
    return _ai_service

@router.post("/chat")
async def chat(
    request: ChatRequest,
    metadata_svc: MetadataService = Depends(get_metadata_service),
    ai_svc: AIService = Depends(get_ai_service)
):
    # Prepare minimal schema context for the AI
    metadata = metadata_svc.get_all_metadata()
    schema_summary = ""
    for table, details in metadata.items():
        cols = ", ".join([c["name"] for c in details["columns"]])
        schema_summary += f"Table {table}: columns ({cols})\n"

    result = ai_svc.generate_sql_from_question(request.question, schema_summary)
    return result
