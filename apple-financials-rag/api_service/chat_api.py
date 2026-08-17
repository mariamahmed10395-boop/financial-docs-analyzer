from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from qdrant_client import QdrantClient
from groq import Groq

# إنشاء تطبيق FastAPI
app = FastAPI(title="Apple Financials RAG API")

# تعريف شكل البيانات اللي هيستقبلها الـ API
class QueryRequest(BaseModel):
    question: str

# ---------------------------------------------------------
# 1. إعداد الاتصال بقاعدة البيانات Qdrant
# ---------------------------------------------------------
qdrant_client = QdrantClient(host="localhost", port=6333)

# ---------------------------------------------------------
# 2. إعداد الاتصال بموديل LLaMA عبر Groq
# ⚠️ ضعي مفتاح Groq الخاص بك هنا بدلاً من "gsk_..."
# ---------------------------------------------------------
GROQ_API_KEY = "gsk_..." 
groq_client = Groq(api_key=GROQ_API_KEY)


@app.get("/")
def health_check():
    return {"status": "✅ API is connected to Qdrant & Groq successfully!"}

@app.post("/ask")
def ask_financial_question(request: QueryRequest):
    if GROQ_API_KEY == "gsk_...":
        raise HTTPException(status_code=500, detail="Please set your Groq API Key in the code.")

    try:
        # --- Phase A: Retrieval (الاسترجاع من قاعدة البيانات) ---
        # بما إننا حفظنا 6 جداول، هنسحبهم كلهم ليكونوا السياق (Context)
        search_result = qdrant_client.scroll(
            collection_name="apple_financials_collection",
            limit=6
        )
        
        tables_data = search_result[0]
        context_text = ""
        for point in tables_data:
            # استخراج محتوى الجدول من الـ Payload
            context_text += f"\nTable Data:\n{point.payload.get('content')}\n"

        # --- Phase B: Augmentation (تجهيز التلقين للموديل) ---
        system_prompt = (
            "You are an expert financial analyst. "
            "Use the provided Apple Q1 2024 financial tables (in JSON format) to answer the user's question accurately. "
            "If the answer is not in the tables, explicitly say 'I cannot find the answer in the provided data'."
            "Keep your answers concise and focus on the numbers."
        )
        
        user_prompt = f"Context:\n{context_text}\n\nQuestion: {request.question}"

        # --- Phase C: Generation (إرسال البيانات لـ LLaMA 3) ---
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="llama3-70b-8192", # استخدام الموديل الأقوى للحسابات
            temperature=0.1, # درجة حرارة منخفضة لضمان دقة الأرقام وعدم الهلوسة
        )

        answer = chat_completion.choices[0].message.content

        return {
            "question": request.question,
            "answer": answer
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))