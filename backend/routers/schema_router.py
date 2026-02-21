from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from backend.services.metadata_service import MetadataService
from backend.services.quality_service import QualityService
from backend.services.ai_service import AIService
from backend.services.export_service import ExportService
from backend.connectors.postgres import PostgresConnector
from backend.config import settings

router = APIRouter()

# Dependency injection for services
def get_postgres_connector():
    return PostgresConnector(settings.DATABASE_URL)

def get_metadata_service(connector = Depends(get_postgres_connector)):
    return MetadataService(connector)

def get_quality_service(connector = Depends(get_postgres_connector)):
    return QualityService(connector)

# Global service instances
_ai_service = AIService()
_export_service = ExportService()

def get_ai_service():
    return _ai_service

def get_export_service():
    return _export_service

@router.get("/metadata")
async def get_metadata(service: MetadataService = Depends(get_metadata_service)):
    return service.get_all_metadata()

@router.get("/quality/{table_name}")
async def get_quality(table_name: str, service: QualityService = Depends(get_quality_service)):
    return service.get_table_quality(table_name)

@router.get("/documentation/{table_name}")
async def get_documentation(
    table_name: str, 
    metadata_svc: MetadataService = Depends(get_metadata_service),
    quality_svc: QualityService = Depends(get_quality_service),
    ai_svc: AIService = Depends(get_ai_service)
):
    metadata = metadata_svc.get_columns(table_name)
    quality = quality_svc.get_table_quality(table_name)
    return ai_svc.generate_table_documentation(table_name, metadata, quality)

@router.get("/export/json")
async def export_json(
    metadata_svc: MetadataService = Depends(get_metadata_service),
    export_svc: ExportService = Depends(get_export_service)
):
    metadata = metadata_svc.get_all_metadata()
    path = export_svc.export_json(metadata, "full_metadata.json")
    return {"message": "Exported to JSON", "path": path}
