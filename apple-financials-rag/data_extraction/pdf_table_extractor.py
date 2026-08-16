import pdfplumber
import pandas as pd
from .extractors_interface import TableExtractor

class PDFTableExtractor(TableExtractor):
    """
    Concrete class responsible for extracting and filtering 
    financial tables from PDF files.
    """
    def extract_tables(self, file_path: str) -> list[pd.DataFrame]:
        extracted_tables = []
        
        print(f"🔍 Scanning {file_path} for tables...")
        
        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages):
                tables = page.extract_tables()
                
                for table in tables:
                    if len(table) > 1: 
                        # تحويل الجدول المستخرج إلى Pandas DataFrame
                        df = pd.DataFrame(table[1:], columns=table[0])
                        
                        # --- Data Cleaning & Filtering ---
                        # 1. إزالة الأعمدة والصفوف الفارغة تماماً
                        df = df.dropna(how='all').dropna(axis=1, how='all')
                        
                        # 2. فلترة الجداول غير المالية:
                        # يجب أن يحتوي الجدول على أكثر من عمود
                        if df.shape[1] > 1:
                            # 3. التأكد من وجود أرقام في الجدول (الفهارس غالباً نصوص)
                            # نستخدم خريطة للبحث عن أي أرقام داخل خلايا الجدول
                            has_numbers = df.map(lambda x: any(char.isdigit() for char in str(x))).any().any()
                            
                            if has_numbers:
                                extracted_tables.append(df)
                        
        print(f"✅ Extracted and filtered down to {len(extracted_tables)} actual financial tables.")
        return extracted_tables