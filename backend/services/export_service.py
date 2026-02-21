import json
import os
from typing import Dict, Any
from backend.config import settings

class ExportService:
    def __init__(self, export_path: str = settings.EXPORT_PATH):
        self.export_path = export_path
        if not os.path.exists(self.export_path):
            os.makedirs(self.export_path)

    def export_json(self, data: Dict[str, Any], filename: str) -> str:
        file_path = os.path.join(self.export_path, filename)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        return file_path

    def export_markdown(self, table_docs: Dict[str, str], filename: str) -> str:
        file_path = os.path.join(self.export_path, filename)
        with open(file_path, 'w') as f:
            f.write("# Data Dictionary Documentation\n\n")
            for table, doc in table_docs.items():
                f.write(f"## Table: {table}\n\n")
                f.write(doc)
                f.write("\n\n---\n\n")
        return file_path
