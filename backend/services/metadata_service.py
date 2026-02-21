from sqlalchemy import Inspector
from typing import List, Dict, Any
from backend.connectors.postgres import PostgresConnector
from backend.config import settings

class MetadataService:
    def __init__(self, connector: PostgresConnector):
        self.connector = connector
        self.inspector = connector.get_inspector()

    def get_all_metadata(self) -> Dict[str, Any]:
        tables = self.inspector.get_table_names()
        metadata = {}

        for table in tables:
            metadata[table] = {
                "columns": self.get_columns(table),
                "primary_keys": self.inspector.get_pk_constraint(table).get("constrained_columns", []),
                "foreign_keys": self.get_foreign_keys(table),
                "indexes": self.inspector.get_indexes(table)
            }
        
        return metadata

    def get_columns(self, table_name: str) -> List[Dict[str, Any]]:
        columns = self.inspector.get_columns(table_name)
        return [
            {
                "name": col["name"],
                "type": str(col["type"]),
                "nullable": col["nullable"],
                "default": str(col["default"]) if col.get("default") else None
            }
            for col in columns
        ]

    def get_foreign_keys(self, table_name: str) -> List[Dict[str, Any]]:
        fks = self.inspector.get_foreign_keys(table_name)
        return [
            {
                "referred_table": fk["referred_table"],
                "referred_columns": fk["referred_columns"],
                "constrained_columns": fk["constrained_columns"]
            }
            for fk in fks
        ]
