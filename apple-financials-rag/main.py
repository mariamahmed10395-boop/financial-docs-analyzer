import os
from data_ingestion.pdf_ingestor import PDFIngestor
from data_extraction.pdf_table_extractor import PDFTableExtractor
from data_storage.qdrant_storage import QdrantStorage

def main():
    file_name = "apple_q1_2024_financials.pdf"
    pdf_path = os.path.join("data", file_name)
    
    # --- Phase 1: Ingestion ---
    print("\n🚀 Starting Phase 1: Data Ingestion...")
    ingestor = PDFIngestor()
    is_valid = ingestor.load_document(pdf_path)
    
    if not is_valid:
        return

    # --- Phase 2: Extraction ---
    print("\n➡️ Proceeding to Phase 2: Extraction...")
    table_extractor = PDFTableExtractor()
    tables = table_extractor.extract_tables(pdf_path)
    
    if not tables:
        print("⚠️ No financial tables found to store.")
        return

    # --- Phase 3: Storage ---
    print("\n💾 Proceeding to Phase 3: Storage...")
    storage = QdrantStorage()
    
    if storage.connect():
        # اسم الـ Collection اللي هنخزن فيه جوه Qdrant
        collection_name = "apple_financials_collection"
        storage.store_tables(collection_name, tables)
        
    print("\n🎉 All phases completed successfully!")

if __name__ == "__main__":
    main()
    