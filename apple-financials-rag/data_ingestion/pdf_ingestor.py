import os
from .interfaces import DocumentIngestor

class PDFIngestor(DocumentIngestor):
    """
    Concrete class responsible exclusively for ingesting PDF files.
    """
    def load_document(self, file_path: str) -> bool:
        # 1. Validation: Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Error: The file {file_path} was not found.")
        
        # 2. Validation: Check if it's actually a PDF
        if not file_path.lower().endswith('.pdf'):
            raise ValueError(f"Error: Invalid format for {file_path}. Expected a PDF.")
        
        # If all checks pass
        print(f"✅ Successfully loaded and validated PDF: {file_path}")
        return True