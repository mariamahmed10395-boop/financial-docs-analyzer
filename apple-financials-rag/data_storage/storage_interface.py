from abc import ABC, abstractmethod
import pandas as pd

class VectorStorage(ABC):
    """
    Interface for storing extracted data into a vector database.
    """
    @abstractmethod
    def connect(self) -> bool:
        """Establishes connection to the database."""
        pass
        
    @abstractmethod
    def store_tables(self, collection_name: str, tables: list[pd.DataFrame]) -> bool:
        """Stores a list of tables into the specified collection."""
        pass