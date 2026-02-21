from abc import ABC, abstractmethod
from sqlalchemy import create_engine, Inspector, inspect
from sqlalchemy.orm import sessionmaker, Session

class BaseConnector(ABC):
    def __init__(self, connection_url: str):
        self.connection_url = connection_url
        self.engine = create_engine(connection_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self) -> Session:
        return self.SessionLocal()

    def get_inspector(self) -> Inspector:
        return inspect(self.engine)

    @abstractmethod
    def get_connection_status(self) -> bool:
        pass
