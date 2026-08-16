# 🍏 Apple Financials RAG System

## 📌 Project Overview
This project is an advanced Retrieval-Augmented Generation (RAG) system specifically designed to ingest, process, and analyze complex financial documents (like Apple's quarterly earnings PDFs). It focuses heavily on accurately extracting financial tables and figures, going beyond simple text extraction.

## 🏗 Architecture (Modular Monolith)
The system is built using a **Modular Monolith** architecture. This ensures clear boundaries between different business domains while keeping the deployment simple. The codebase strictly adheres to **SOLID principles** and utilizes standard **Design Patterns** (LLD) for maintainability and scalability.

## 🚀 High-Level Design (HLD) & Implementation Phases

The project development is divided into 5 distinct phases:

### Phase 1: Data Ingestion 📥
* Collecting and loading financial PDF reports (e.g., 10-Q, 10-K statements) from Apple Investor Relations.
* Managing file streams and input validation.

### Phase 2: Extraction & Processing ⚙️
* **Text Parsing:** Extracting contextual financial paragraphs.
* **Table Extraction:** Specialized handling for financial tables and numbers to maintain their tabular structure and meaning.
* **Chunking:** Preparing the extracted data for vectorization.

### Phase 3: Storage (Vector & Metadata) 💾
* Vectorizing chunks and storing them in a Vector Database (e.g., Qdrant).
* Storing document metadata for enhanced filtering and retrieval.

### Phase 4: API Layer 🔌
* Building a RESTful API (using FastAPI) to handle user queries.
* Integrating the retrieval engine with a Large Language Model (LLM) to formulate accurate, data-backed answers based on the financial reports.

### Phase 5: Deployment & Orchestration 🐳
* Containerizing the entire application using **Docker**.
* Using **Docker Compose** to orchestrate the backend, vector database, and any other required services seamlessly.

## 🛠 Technologies Used
* **Language:** Python
* **Architecture:** Modular Monolith, OOP, SOLID Principles
* **Framework:** FastAPI (Phase 4)
* **Orchestration:** Docker & Docker Compose
* **Vector DB:** Qdrant (or similar)