from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import pandas as pd
import uuid
from .storage_interface import VectorStorage

class QdrantStorage(VectorStorage):
    def __init__(self, host: str = "localhost", port: int = 6333):
        self.host = host
        self.port = port
        self.client = None

    def connect(self) -> bool:
        try:
            self.client = QdrantClient(host=self.host, port=self.port)
            print(f"✅ Successfully connected to Qdrant at {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"❌ Failed to connect to Qdrant: {e}")
            return False

    def store_tables(self, collection_name: str, tables: list[pd.DataFrame]) -> bool:
        if not self.client:
            print("❌ Error: Not connected to Qdrant.")
            return False
            
        # إنشاء Collection لو مش موجود
        if not self.client.collection_exists(collection_name=collection_name):
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )
            print(f"📁 Created new collection: '{collection_name}'")

        points = []
        for i, df in enumerate(tables):
            # تحويل الجدول لنص عشان يتخزن كبيانات وصفية (Payload)
            table_json = df.to_json(orient="split")
            
            # متجه وهمي (Dummy Vector) لاختبار التخزين فقط
            dummy_vector = [0.1] * 384 
            
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=dummy_vector,
                payload={
                    "table_index": i, 
                    "content": table_json, 
                    "source": "Apple Q1 2024"
                }
            )
            points.append(point)
        
        # رفع البيانات لقاعدة البيانات
        if points:
            self.client.upsert(
                collection_name=collection_name,
                points=points
            )
            print(f"💾 Successfully stored {len(points)} tables in Qdrant collection '{collection_name}'.")
        
        return True