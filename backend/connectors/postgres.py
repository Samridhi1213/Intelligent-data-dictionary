from .base import BaseConnector
from sqlalchemy import text

class PostgresConnector(BaseConnector):
    def get_connection_status(self) -> bool:
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            print(f"PostgreSQL connection error: {e}")
            return False
