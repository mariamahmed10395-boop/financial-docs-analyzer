import os
from data_ingestion.pdf_ingestor import PDFIngestor
from data_extraction.pdf_table_extractor import PDFTableExtractor

def main():
    file_name = "apple_q1_2024_financials.pdf"
    pdf_path = os.path.join("data", file_name)
    
    # --- Phase 1: Ingestion ---
    print("🚀 Starting Phase 1: Data Ingestion...")
    ingestor = PDFIngestor()
    
    try:
        is_valid = ingestor.load_document(pdf_path)
        
        if is_valid:
            print("➡️ Proceeding to Phase 2 (Extraction)...\n")
            
            # --- Phase 2: Extraction ---
            table_extractor = PDFTableExtractor()
            tables = table_extractor.extract_tables(pdf_path)
            
        
            if tables:
                print("\n📊 First extracted table preview:")
                print("-----------------------------------")
                print(tables[0].head())
            else:
                print("⚠️ No tables found in the document.")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()