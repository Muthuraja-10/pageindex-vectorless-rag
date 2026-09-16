# PageIndex RAG

A PageIndex-based Vectorless RAG system that retrieves relevant information from documents using page indexing, section indexing, and keyword matching instead of embeddings or vector databases.

The system uses FastAPI, Oracle Database, Groq LLM, and React to provide a document question-answering workflow with structured document understanding.

## 🚀 Overview

Traditional RAG systems commonly use embeddings and vector databases to retrieve relevant document chunks.

This project takes a different approach:

```text
                    ┌─────────────────────┐
                    │    PDF Document     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   PDF Text Extract  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Page Indexing    │
                    │  Page 1, Page 2...  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Section Detection  │
                    │      Groq LLM       │
                    └──────────┬──────────┘
                               │
                               ▼
             ┌──────────────────────────────────┐
             │           Section Index           │
             │                                    │
             │ • Section Title                   │
             │ • Section Summary                 │
             │ • Start Page                      │
             │ • End Page                        │
             │ • Keywords                        │
             └────────────────┬───────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    User Question    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Keyword Extraction  │
                    │      Groq LLM       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Keyword Retrieval   │
                    │     Oracle DB       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Relevant Sections  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Relevant Page Data │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Groq Answer LLM   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Final Answer    │
                    └─────────────────────┘
```

## ✨ Features

- 📄 PDF document upload
- 📑 Page-level document indexing
- 🧩 Automatic section detection
- 📝 Section summaries generated using LLM
- 🔑 Automatic keyword extraction
- 🔎 Keyword-based retrieval
- 📚 Section-based context retrieval
- 🤖 Groq-powered question answering
- 🗄️ Oracle Database persistence
- ⚡ FastAPI REST API
- ⚛️ React frontend
- 🚫 No embeddings
- 🚫 No vector database
- 🚫 No semantic vector similarity
- 🏗️ Repository → Service → API architecture

## 🧠 Why PageIndex RAG?

The main idea is to make document retrieval more structured and explainable.

Instead of:

```text
Question
   ↓
Embedding
   ↓
Vector Search
   ↓
Top-K Chunks
   ↓
LLM
```

this project uses:

```text
Question
   ↓
Question Keywords
   ↓
Keyword Index
   ↓
Relevant Sections
   ↓
Section Page Range
   ↓
Relevant Pages
   ↓
LLM
```

The system therefore knows which section and which pages are being used to construct the answer.

## 🏗️ Architecture

### Backend Architecture

```text
FastAPI
   │
   ├── API Layer
   │      ├── Upload API
   │      ├── Ask API
   │      └── Retrieval APIs
   │
   ├── Service Layer
   │      ├── DocumentService
   │      ├── PageService
   │      ├── SectionService
   │      ├── RetrieverService
   │      └── GroqService
   │
   ├── Repository Layer
   │      ├── DocumentRepository
   │      ├── PageRepository
   │      ├── SectionRepository
   │      └── KeywordRepository
   │
   └── Oracle Database
          ├── page_documents
          ├── page_pages
          ├── page_sections
          └── page_section_keywords
```

## 🔄 Document Ingestion Pipeline

When a PDF is uploaded:

### 1. Document Upload

The PDF is uploaded through the FastAPI `/upload` endpoint.

```text
PDF
 ↓
FastAPI
 ↓
Save File
 ↓
Create Document Record
```

### 2. Page Extraction

PyMuPDF extracts text page by page.

```text
PDF
│
├── Page 1 → Text
├── Page 2 → Text
├── Page 3 → Text
└── Page N → Text
```

Each page is stored separately in Oracle.

### 3. Section Detection

The extracted document pages are sent to Groq.

The LLM identifies:

- Section Title
- Section Summary
- Keywords
- Start Page
- End Page

Example:

```json
{
  "section_title": "Introduction",
  "section_summary": "Overview of cloud computing concepts",
  "keywords": [
    "Cloud Computing",
    "Virtualization",
    "Infrastructure"
  ],
  "start_page": 1,
  "end_page": 3
}
```

### 4. Section Indexing

The detected sections are stored in Oracle in `page_sections`.

Keywords are stored separately in `page_section_keywords`.

This creates the searchable section index.

## 🔍 Retrieval Pipeline

When the user asks a question, for example:

> "What is CAPEX?"

### Step 1 — Extract Search Keywords

Groq extracts important terms:

```
CAPEX
```

### Step 2 — Keyword Search

The keyword index is searched in Oracle.

```text
CAPEX
 ↓
page_section_keywords
 ↓
Matching Section IDs
```

### Step 3 — Retrieve Sections

The matching section information is retrieved:

- Section Title
- Section Summary
- Start Page
- End Page

### Step 4 — Retrieve Pages

The section's page range is used to retrieve the original page content.

```text
Section:
Cloud Infrastructure

Pages:
10 → 14
```

### Step 5 — Generate Answer

The retrieved context is sent to Groq.

```text
Relevant Section
      +
Relevant Pages
      +
User Question
      ↓
    Groq
      ↓
Final Answer
```

## 🗄️ Database Design

### `page_documents`

Stores uploaded documents.

| Column | Description |
|---|---|
| document_id | Unique document ID |
| file_name | Uploaded file name |
| file_path | Stored file path |

### `page_pages`

Stores page-level content.

| Column | Description |
|---|---|
| page_id | Unique page ID |
| document_id | Parent document |
| page_number | Page number |
| page_content | Extracted text |

### `page_sections`

Stores detected sections.

| Column | Description |
|---|---|
| section_id | Unique section ID |
| document_id | Parent document |
| section_title | Section name |
| section_summary | LLM-generated summary |
| start_page | Starting page |
| end_page | Ending page |

### `page_section_keywords`

Stores keywords associated with sections.

| Column | Description |
|---|---|
| keyword_id | Unique keyword ID |
| section_id | Related section |
| keyword | Search keyword |

## 🛠️ Tech Stack

**Backend**
- Python
- FastAPI
- Pydantic
- Uvicorn

**LLM**
- Groq API
- Llama models

**Database**
- Oracle Database
- oracledb Python driver

**Document Processing**
- PyMuPDF / Fitz

**Frontend**
- React
- Tailwind CSS

**Architecture**
- REST API
- Repository Pattern
- Service Layer
- Page Indexing
- Section Indexing
- Keyword Retrieval

## 📁 Project Structure

```text
PageRAG/
│
├── backend/
│   │
│   ├── app/
│   │   ├── api/
│   │   │   ├── upload_routes.py
│   │   │   └── query_routes.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── database.py
│   │   │
│   │   ├── repositories/
│   │   │   ├── document_repository.py
│   │   │   ├── page_repository.py
│   │   │   ├── section_repository.py
│   │   │   └── keyword_repository.py
│   │   │
│   │   ├── services/
│   │   │   ├── document_service.py
│   │   │   ├── page_service.py
│   │   │   ├── section_service.py
│   │   │   ├── groq_service.py
│   │   │   └── retriever_service.py
│   │   │
│   │   ├── utils/
│   │   │   └── pdf_reader.py
│   │   │
│   │   ├── uploads/
│   │   │
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   └── React application
│
└── README.md
```

## 🔌 API Endpoints

### Health Check

`GET /`

Checks whether the API is running.

### Upload Document

`POST /upload`

Uploads and processes a PDF document.

Processing:

```text
Upload
 ↓
Document Creation
 ↓
Page Extraction
 ↓
Page Storage
 ↓
Section Detection
 ↓
Section Storage
 ↓
Keyword Storage
```

### Ask Question

`POST /ask`

Example request:

```json
{
  "question": "What is CAPEX?"
}
```

Example response:

```json
{
  "question": "What is CAPEX?",
  "answer": "CAPEX refers to Capital Expenditure..."
}
```

### Get Pages

`GET /pages/{document_id}/pages`

Returns the number of indexed pages for a document.

### Get Section Information

`GET /section-info/{section_id}`

Returns information about a specific section.

Example:

```json
{
  "document_id": 62,
  "section_title": "Cloud Infrastructure",
  "section_summary": "Overview of cloud infrastructure...",
  "start_page": 10,
  "end_page": 14
}
```

### Get Pages Between Range

`GET /pages-between/{document_id}/{start}/{end}`

Retrieves page content between a specified page range.

Example:

```
GET /pages-between/62/10/14
```

## ⚙️ Installation

### 1. Clone Repository

```
git clone https://github.com/Muthuraja-10/PageRAG.git
cd PageRAG
```

### 2. Create Virtual Environment

```
python -m venv venv
```

Windows:

```
venv\Scripts\activate
```

Linux / macOS:

```
source venv/bin/activate
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

## 🔐 Environment Variables

Create a `.env` file:

```
GROQ_API_KEY=your_groq_api_key

ORACLE_USER=your_oracle_username
ORACLE_PASSWORD=your_oracle_password
ORACLE_DSN=your_oracle_dsn
```

Do not commit `.env` to GitHub. Add `.env` to `.gitignore`.

## ▶️ Run Backend

From the backend directory:

```
uvicorn app.main:app --reload
```

API: `http://127.0.0.1:8000`

Swagger documentation: `http://127.0.0.1:8000/docs`

## ▶️ Run Frontend

```
cd frontend
npm install
npm run dev
```

## 🧪 Example Workflow

Upload:

```
POST /upload
```

The system processes:

```text
Document
   ↓
113 Pages
   ↓
Page Index
   ↓
Section Detection
   ↓
Section Index
   ↓
Keyword Index
```

Then the user can ask:

> "What is CAPEX?"

The system performs:

```text
Question
   ↓
CAPEX
   ↓
Keyword Search
   ↓
Matching Section
   ↓
Relevant Pages
   ↓
Groq
   ↓
Answer
```

## 📊 Retrieval Strategy

This project intentionally avoids vector similarity.

| Feature | PageIndex RAG |
|---|---|
| Embeddings | ❌ |
| Vector DB | ❌ |
| FAISS | ❌ |
| Chroma | ❌ |
| Cosine Similarity | ❌ |
| Page Index | ✅ |
| Section Index | ✅ |
| Keyword Index | ✅ |
| Oracle DB | ✅ |
| LLM | Groq |

The LLM is used for document understanding and answer generation, while Oracle performs the structured retrieval.

## 🎯 Design Goals

The project focuses on:

- Structured document understanding
- Explainable retrieval
- Page-aware context
- Section-aware retrieval
- Reduced dependency on vector databases
- Simple database-driven retrieval
- Clear backend architecture
- Enterprise document question answering

## 🚧 Current Development

### Completed

- [x] PDF upload
- [x] Document storage
- [x] Page extraction
- [x] Page indexing
- [x] Section detection
- [x] Section summaries
- [x] Keyword extraction
- [x] Keyword indexing
- [x] Keyword retrieval
- [x] Section retrieval
- [x] Page-range retrieval
- [x] Groq answer generation
- [x] Oracle CLOB handling
- [x] FastAPI APIs
- [x] React frontend integration groundwork

### Planned Improvements

- [ ] Batch processing for large documents
- [ ] Context-size management
- [ ] Multi-document retrieval
- [ ] Keyword normalization
- [ ] Retrieval ranking
- [ ] Chat history
- [ ] Session-based conversations
- [ ] Authentication and authorization
- [ ] Source/page references in answers
- [ ] Admin/document management interface

## 🔮 Future Direction

The project can be extended toward a more advanced enterprise retrieval architecture:

```text
PageIndex RAG
      ↓
Hybrid Search
      ↓
Agentic RAG
      ↓
Graph RAG
      ↓
Long-Term Conversational Memory
```

Possible future improvements include combining:

```text
Keyword Search
      +
BM25
      +
Vector Search
      +
Graph Relationships
      +
Agentic Retrieval
```

## 👨‍💻 Author

**Muthuraja P**

Computer Science & Engineering
Anna University – BIT Campus, Trichy

Areas of Interest:
- Backend Engineering
- FastAPI
- Artificial Intelligence
- RAG Systems
- Generative AI
- Information Retrieval
- Database Systems
- Software Engineering

## ⭐ Project Summary

PageIndex RAG is a vectorless document question-answering system that uses page indexing, section indexing, keyword retrieval, Oracle Database, and Groq LLMs to retrieve and generate answers from PDF documents.
