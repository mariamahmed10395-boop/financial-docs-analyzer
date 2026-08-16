from abc import ABC, abstractmethod
import pandas as pd

class TableExtractor(ABC):
    """
    Interface for extracting tables from documents.
    """
    @abstractmethod
    def extract_tables(self, file_path: str) -> list[pd.DataFrame]:
        """
        Extracts tables from the file and returns them as a list of Pandas DataFrames.
        """
        pass