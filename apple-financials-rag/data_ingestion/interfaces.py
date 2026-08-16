from abc import ABC, abstractmethod

class DocumentIngestor(ABC):
    """
    Interface for handling document ingestion.
    """
    @abstractmethod
    def load_document(self, file_path: str) -> bool:
        """
        Loads and validates the document.
        Returns True if valid, raises exceptions otherwise.
        """
        pass